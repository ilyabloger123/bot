import asyncio
import logging
import sys
import os

from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update
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

bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher()

dp.include_router(start_router)
dp.include_router(help_router)
dp.include_router(password_router)
dp.include_router(inline_router)
dp.include_router(settings_router)

WEBHOOK_PATH = f"/webhook/{Config.BOT_TOKEN}/"
WEBHOOK_URL = os.getenv("RENDER_EXTERNAL_URL") + WEBHOOK_PATH

async def handle_webhook(request):
    try:
        update_data = await request.json()
        update = Update(**update_data)
        await dp.feed_update(bot, update)
        return web.json_response({"status": "ok"})
    except Exception as e:
        logger.error(f"main.py 45: {e}")
        return web.json_response({"error": str(e)}, status=500)

async def on_startup(app):
    await bot.set_webhook(url=WEBHOOK_URL)
    logger.info(f"Webhook set to {WEBHOOK_URL}")

async def on_shutdown(app):
    await bot.delete_webhook()
    await bot.session.close()

def main():
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, handle_webhook)
    app.router.add_get("/", lambda r: web.json_response({"status": "running"}))
    app.router.add_get("/health", lambda r: web.json_response({"status": "ok"}))

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    port = int(os.getenv("PORT", 8080))
    logger.info(f"Running on port {port}")
    web.run_app(app, port=port, host="0.0.0.0")

if __name__ == "__main__":
    main()
