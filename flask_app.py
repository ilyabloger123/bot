import sys
import os
import asyncio

from flask import Flask, request, jsonify

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Update

project_home = "/home/ilyabloger123/password_bot"
if project_home not in sys.path:
    sys.path.append(project_home)

from config import Config

from handlers.start import router as start_router
from handlers.help import router as help_router
from handlers.password_handlers import router as password_router
from handlers.inline_handlers import router as inline_router
from handlers.settings_handler import router as settings_router

bot = Bot(token=Config.BOT_TOKEN, default=DefaultBotProperties(link_preview_is_disabled=True))
dp = Dispatcher()

dp.include_router(start_router)
dp.include_router(help_router)
dp.include_router(password_router)
dp.include_router(inline_router)
dp.include_router(settings_router)

app = Flask(__name__)

@app.route(f"/webhook/{Config.BOT_TOKEN}", methods=["POST"])
async def webhook():
    """end point куда телеграм будет присылать обновления"""
    try:
        update_data = request.get_json()
        update = Update(**update_data)
        await dp.feed_update(bot, update)
        return jsonify({"status": "ok"})
    except Exception as e:
        print(f"Ошибка:{e}")
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
async def index():
    return "Бот работает"

application = app
