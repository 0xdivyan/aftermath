import aiohttp
from typing import Dict, List, Optional
from loguru import logger
from datetime import datetime
from config.settings import settings
from src.core.models import PolymarketOrder, PolymarketMarket, TradeStatus


class PolymarketClient:
    """Polymarket CLOB API client"""
    
    def __init__(self, api_key: str, private_key: str):
        self.api_key = api_key
        self.private_key = private_key
        self.base_url = settings.polymarket_clob_url
        self.wallet_balance = settings.initial_balance
        self.timeout = aiohttp.ClientTimeout(total=settings.request_timeout_seconds)
        
    async def get_markets(self, query: str) -> List[PolymarketMarket]:
        """Search for earnings-related markets"""
        # Note: Actual Polymarket API endpoint may differ
        url = f"{self.base_url}/markets"
        params = {"query": query}
        
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(url, params=params) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        markets = []
                        
                        for m in data:
                            market = PolymarketMarket(
                                market_id=m.get('id', ''),
                                question=m.get('question', ''),
                                ticker=query.split()[0],
                                end_date=datetime.fromisoformat(m.get('end_date', '')),
                                volume=float(m.get('volume', 0)),
                                liquidity=float(m.get('liquidity', 0))
                            )
                            markets.append(market)
                        
                        logger.info(f"Found {len(markets)} markets for '{query}'")
                        return markets
                    else:
                        logger.warning(f"No markets found for '{query}'")
                        return []
        except Exception as e:
            logger.error(f"Error fetching markets: {e}")
            return []
    
    async def get_order_book(self, market_id: str, outcome: str) -> Dict:
        """Get current order book"""
        url = f"{self.base_url}/book"
        params = {
            "token_id": market_id,
            "side": "BUY" if outcome == "Yes" else "SELL"
        }
        
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(url, params=params) as resp:
                    if resp.status == 200:
                        return await resp.json()
        except Exception as e:
            logger.error(f"Error fetching order book: {e}")
        
        return {}
    
    def calculate_potential_return(self, price: float) -> float:
        """Calculate potential return %"""
        if price == 0:
            return 0
        payout = 1.0
        return ((payout - price) / price) * 100
    
    async def execute_trade(self, order: PolymarketOrder) -> bool:
        """Execute trade on Polymarket"""
        trade_size = self.wallet_balance * (settings.trade_allocation_percentage / 100)
        
        if trade_size > settings.max_position_size:
            logger.warning(f"Trade size {trade_size} exceeds max {settings.max_position_size}")
            return False
        
        logger.info(f"🎯 Executing: {order.outcome} @ ${order.price:.4f}, "
                   f"Size: ${trade_size:.2f}, Expected: +{order.potential_return:.2f}%")
        
        # TODO: Integrate py-clob-client for actual execution
        """
        from py_clob_client.client import ClobClient
        from py_clob_client.clob_types import OrderArgs
        
        client = ClobClient(
            host=self.base_url,
            key=self.private_key,
            chain_id=settings.polymarket_chain_id
        )
        
        order_args = OrderArgs(
            price=order.price,
            size=trade_size,
            side=BUY,
            token_id=order.market_id
        )
        
        signed_order = client.create_and_sign_order(order_args)
        resp = await client.post_order(signed_order)
        """
        
        # Simulation
        logger.success(f"✅ Trade executed successfully!")
        order.status = TradeStatus.EXECUTED
        return True
    
    async def get_wallet_balance(self) -> float:
        """Get current wallet balance"""
        # TODO: Implement actual balance check
        return self.wallet_balance