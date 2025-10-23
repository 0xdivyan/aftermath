from typing import Optional
from loguru import logger
from src.core.models import EarningsOutcome, PolymarketOrder


class TradingStrategy:
    """Trading strategy logic"""
    
    def __init__(self):
        self.win_count = 0
        self.loss_count = 0
        self.total_pnl = 0.0
    
    def should_trade(self, outcome: EarningsOutcome, price: float, 
                    potential_return: float, min_threshold: float) -> bool:
        """Determine if trade should be executed"""
        
        if outcome == EarningsOutcome.UNKNOWN:
            logger.warning("Cannot trade on unknown outcome")
            return False
        
        if potential_return < min_threshold:
            logger.info(f"Return {potential_return:.2f}% below threshold {min_threshold}%")
            return False
        
        if price <= 0 or price >= 1:
            logger.warning(f"Invalid price: {price}")
            return False
        
        return True
    
    def calculate_position_size(self, balance: float, allocation_pct: float, 
                               max_position: float) -> float:
        """Calculate position size with risk limits"""
        size = balance * (allocation_pct / 100)
        return min(size, max_position)
    
    def record_trade(self, pnl: float):
        """Record trade outcome"""
        self.total_pnl += pnl
        
        if pnl > 0:
            self.win_count += 1
        else:
            self.loss_count += 1
    
    def get_stats(self) -> dict:
        """Get strategy statistics"""
        total_trades = self.win_count + self.loss_count
        win_rate = (self.win_count / total_trades * 100) if total_trades > 0 else 0
        
        return {
            "total_trades": total_trades,
            "wins": self.win_count,
            "losses": self.loss_count,
            "win_rate": win_rate,
            "total_pnl": self.total_pnl
        }
