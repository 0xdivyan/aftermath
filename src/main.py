import asyncio
import signal
from loguru import logger
from config.settings import settings
from src.core.bot import AftermathBot
from src.utils.logger import setup_logging


async def shutdown(bot: AftermathBot):
    """Graceful shutdown handler"""
    logger.info("Shutting down bot...")
    await bot.stop()
    logger.info("Bot stopped successfully")


async def main():
    """Main entry point"""
    # Setup logging
    setup_logging(settings.log_level)
    
    logger.info("=" * 60)
    logger.info("🚀 Aftermath Bot Starting...")
    logger.info("=" * 60)
    logger.info(f"Version: 1.0.0")
    logger.info(f"Wallet: {settings.wallet_address}")
    logger.info(f"Initial Balance: ${settings.initial_balance}")
    logger.info(f"Trade Allocation: {settings.trade_allocation_percentage}%")
    logger.info(f"Min Return Threshold: {settings.min_return_threshold}%")
    logger.info("=" * 60)
    
    # Initialize bot
    bot = AftermathBot(
        polygon_key=settings.polygon_api_key,
        polymarket_key=settings.polymarket_api_key,
        polymarket_private_key=settings.polymarket_private_key
    )
    
    # Setup signal handlers for graceful shutdown
    loop = asyncio.get_event_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(
            sig,
            lambda: asyncio.create_task(shutdown(bot))
        )
    
    try:
        # Run bot
        await bot.run()
    except KeyboardInterrupt:
        logger.info("Received interrupt signal")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
    finally:
        await shutdown(bot)


if __name__ == "__main__":
    asyncio.run(main())