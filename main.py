import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from config import Config
from handlers.start import router as start_router
from handlers.help import router as help_router
from handlers.password_handlers import router as password_router
from handlers.inline_handlers import router as inline_router
from handlers.settings_handler import router as settings_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers = [
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

async def main():
    bot = Bot(token=Config.BOT_TOKEN, default=DefaultBotProperties(link_preview_is_disabled=True))
    dp = Dispatcher()
    dp.include_router(start_router)
    dp.include_router(help_router)
    dp.include_router(password_router)
    dp.include_router(inline_router)
    dp.include_router(settings_router)
    logger.info("Starting bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

