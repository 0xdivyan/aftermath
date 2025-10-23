from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class EarningsOutcome(Enum):
    BEAT = "beat"
    MISS = "miss"
    INLINE = "inline"
    UNKNOWN = "unknown"


class TradeStatus(Enum):
    PENDING = "pending"
    EXECUTED = "executed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class EarningsEvent:
    ticker: str
    company_name: str
    earnings_date: datetime
    expected_eps: Optional[float] = None
    actual_eps: Optional[float] = None
    outcome: EarningsOutcome = EarningsOutcome.UNKNOWN
    verified_at: Optional[datetime] = None


@dataclass
class PolymarketMarket:
    market_id: str
    question: str
    ticker: str
    end_date: datetime
    volume: float = 0.0
    liquidity: float = 0.0


@dataclass
class PolymarketOrder:
    market_id: str
    outcome: str  # "Yes" or "No"
    price: float
    size: float
    potential_return: float
    created_at: datetime = field(default_factory=datetime.now)
    status: TradeStatus = TradeStatus.PENDING


@dataclass
class Trade:
    order: PolymarketOrder
    execution_time: Optional[float] = None
    actual_return: Optional[float] = None
    executed_at: Optional[datetime] = None
    error: Optional[str] = None