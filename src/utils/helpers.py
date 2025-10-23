from datetime import datetime, timedelta
from typing import Optional


def calculate_return_percentage(entry_price: float, exit_price: float) -> float:
    """Calculate return percentage"""
    if entry_price == 0:
        return 0.0
    return ((exit_price - entry_price) / entry_price) * 100


def is_market_hours() -> bool:
    """Check if US market is open (rough approximation)"""
    now = datetime.now()
    if now.weekday() >= 5:  # Weekend
        return False
    
    hour = now.hour
    if 9 <= hour < 16:  # 9 AM to 4 PM ET (simplified)
        return True
    return False


def format_currency(amount: float) -> str:
    """Format amount as USD"""
    return f"${amount:,.2f}"


def time_until(target: datetime) -> str:
    """Human-readable time until target"""
    delta = target - datetime.now()
    
    if delta.total_seconds() < 0:
        return "Past"
    
    days = delta.days
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60
    
    if days > 0:
        return f"{days}d {hours}h"
    elif hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"