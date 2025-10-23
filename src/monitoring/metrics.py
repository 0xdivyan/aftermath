from prometheus_client import Counter, Histogram, Gauge, start_http_server
from loguru import logger
from config.settings import settings


# Metrics
trades_executed = Counter('aftermath_trades_executed_total', 'Total trades executed')
trades_successful = Counter('aftermath_trades_successful_total', 'Successful trades')
trades_failed = Counter('aftermath_trades_failed_total', 'Failed trades')

execution_time = Histogram('aftermath_execution_seconds', 'Trade execution time')
verification_time = Histogram('aftermath_verification_seconds', 'Earnings verification time')

wallet_balance = Gauge('aftermath_wallet_balance_usd', 'Current wallet balance')
total_pnl = Gauge('aftermath_total_pnl_usd', 'Total profit/loss')
active_positions = Gauge('aftermath_active_positions', 'Number of active positions')


def start_metrics_server():
    """Start Prometheus metrics server"""
    if settings.enable_metrics:
        try:
            start_http_server(settings.metrics_port)
            logger.info(f"📊 Metrics server started on port {settings.metrics_port}")
        except Exception as e:
            logger.error(f"Failed to start metrics server: {e}")


def record_trade_executed():
    trades_executed.inc()


def record_trade_success():
    trades_successful.inc()


def record_trade_failure():
    trades_failed.inc()


def record_execution_time(seconds: float):
    execution_time.observe(seconds)


def record_verification_time(seconds: float):
    verification_time.observe(seconds)


def update_wallet_balance(balance: float):
    wallet_balance.set(balance)


def update_total_pnl(pnl: float):
    total_pnl.set(pnl)


def update_active_positions(count: int):
    active_positions.set(count)