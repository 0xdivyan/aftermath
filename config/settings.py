from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Polygon.io
    polygon_api_key: str
    polygon_base_url: str = "https://api.polygon.io"
    
    # Polymarket
    polymarket_api_key: str
    polymarket_clob_url: str = "https://clob.polymarket.com"
    polymarket_private_key: str
    polymarket_chain_id: int = 137
    
    # Wallet
    wallet_address: str
    initial_balance: float = 100.0
    
    # Trading
    trade_allocation_percentage: float = 10.0
    min_return_threshold: float = 5.0
    
    # Risk Management
    max_concurrent_trades: int = 3
    max_daily_trades: int = 20
    max_position_size: float = 50.0
    
    # Performance
    scan_interval_seconds: int = 60
    earnings_check_window_minutes: int = 5
    request_timeout_seconds: int = 5
    max_retries: int = 3
    
    # Monitoring
    log_level: str = "INFO"
    enable_metrics: bool = True
    metrics_port: int = 8080
    
    # Notifications (Optional)
    telegram_bot_token: Optional[str] = None
    telegram_chat_id: Optional[str] = None
    discord_webhook_url: Optional[str] = None
    
    # Database (Optional)
    database_url: str = "sqlite:///aftermath.db"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
