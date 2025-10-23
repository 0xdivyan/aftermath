import asyncio
from datetime import datetime, timedelta
from typing import Dict, List
from loguru import logger
from config.settings import settings
from src.api.polygon_client import PolygonAPIClient
from src.api.polymarket_client import PolymarketClient
from src.core.models import EarningsEvent, EarningsOutcome, PolymarketOrder
from src.core.strategy import TradingStrategy


class AftermathBot:
    """Main bot orchestrator"""
    
    def __init__(self, polygon_key: str, polymarket_key: str, polymarket_private_key: str):
        self.polygon = PolygonAPIClient(polygon_key)
        self.polymarket = PolymarketClient(polymarket_key, polymarket_private_key)
        self.strategy = TradingStrategy()
        
        self.tracked_events: Dict[str, EarningsEvent] = {}
        self.active_trades: List[PolymarketOrder] = []
        self.daily_trade_count = 0
        self.is_running = False
        
    async def scan_upcoming_earnings(self):
        """Scan and track upcoming earnings"""
        logger.info("📊 Scanning earnings calendar...")
        calendar = await self.polygon.get_earnings_calendar(days_ahead=7)
        
        new_count = 0
        for event in calendar:
            ticker = event.get('ticker')
            if not ticker or ticker in self.tracked_events:
                continue
            
            # Check for Polymarket markets
            markets = await self.polymarket.get_markets(f"{ticker} earnings")
            
            if markets:
                earnings_event = EarningsEvent(
                    ticker=ticker,
                    company_name=event.get('company_name', ticker),
                    earnings_date=datetime.fromisoformat(event.get('period_of_report_date', ''))
                )
                self.tracked_events[ticker] = earnings_event
                new_count += 1
                logger.info(f"📌 Tracking {ticker} - {len(markets)} market(s) found")
        
        logger.info(f"📊 Tracking {len(self.tracked_events)} total events ({new_count} new)")
    
    async def verify_and_trade(self, ticker: str):
        """Ultra-fast verification and execution pipeline"""
        start = datetime.now()
        
        # Step 1: Verify outcome
        logger.info(f"⚡ Verifying {ticker}...")
        event = await self.polygon.verify_earnings_outcome(ticker)
        
        if not event:
            logger.warning(f"❌ Could not verify {ticker}")
            return
        
        # Determine outcome (simplified - needs consensus data)
        # For now, assume beat if EPS > 0, miss if < 0
        if event.actual_eps and event.actual_eps > 0:
            event.outcome = EarningsOutcome.BEAT
        else:
            event.outcome = EarningsOutcome.MISS
        
        verify_time = (datetime.now() - start).total_seconds()
        logger.info(f"✓ Verified in {verify_time:.3f}s: {event.outcome.value}")
        
        # Step 2: Find markets
        markets = await self.polymarket.get_markets(f"{ticker} earnings beat")
        if not markets:
            logger.warning(f"No markets for {ticker}")
            return
        
        # Step 3: Execute strategy
        target_outcome = "Yes" if event.outcome == EarningsOutcome.BEAT else "No"
        
        for market in markets:
            order_book = await self.polymarket.get_order_book(market.market_id, target_outcome)
            
            if not order_book:
                continue
            
            asks = order_book.get('asks', [])
            if not asks:
                continue
            
            best_price = float(asks[0].get('price', 0))
            potential_return = self.polymarket.calculate_potential_return(best_price)
            
            # Check if meets threshold
            if potential_return >= settings.min_return_threshold:
                # Check daily limits
                if self.daily_trade_count >= settings.max_daily_trades:
                    logger.warning(f"⚠️ Daily trade limit reached ({settings.max_daily_trades})")
                    return
                
                if len(self.active_trades) >= settings.max_concurrent_trades:
                    logger.warning(f"⚠️ Max concurrent trades reached ({settings.max_concurrent_trades})")
                    return
                
                # Execute
                order = PolymarketOrder(
                    market_id=market.market_id,
                    outcome=target_outcome,
                    price=best_price,
                    size=self.polymarket.wallet_balance * 0.10,
                    potential_return=potential_return
                )
                
                success = await self.polymarket.execute_trade(order)
                
                if success:
                    self.active_trades.append(order)
                    self.daily_trade_count += 1
                    
                    total_time = (datetime.now() - start).total_seconds()
                    logger.success(f"⚡ Total execution: {total_time:.3f}s")
                    break
            else:
                logger.info(f"📉 Return {potential_return:.2f}% < threshold {settings.min_return_threshold}%")
    
    async def monitor_loop(self):
        """Main monitoring loop"""
        logger.info("👀 Starting monitor loop...")
        
        while self.is_running:
            try:
                now = datetime.now()
                
                # Check tracked events
                for ticker, event in list(self.tracked_events.items()):
                    time_diff = (event.earnings_date - now).total_seconds()
                    
                    # Within earnings window
                    window = settings.earnings_check_window_minutes * 60
                    if -window <= time_diff <= 0:
                        logger.info(f"🔔 Earnings released for {ticker}!")
                        await self.verify_and_trade(ticker)
                        del self.tracked_events[ticker]
                
                # Refresh calendar periodically
                await asyncio.sleep(settings.scan_interval_seconds)
                
            except Exception as e:
                logger.error(f"Error in monitor loop: {e}")
                await asyncio.sleep(10)
    
    async def run(self):
        """Start the bot"""
        self.is_running = True
        
        # Initial scan
        await self.scan_upcoming_earnings()
        
        # Start monitoring
        await self.monitor_loop()
    
    async def stop(self):
        """Stop the bot gracefully"""
        self.is_running = False
        logger.info("Bot stopped")