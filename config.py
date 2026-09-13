import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    PYTHONANYWHERE_USERNAME = "ilyabloger123"
    PASSWORD_FILE = "password.json"

    DEFAULT_PASSWORD_LENGTH = 16
    MIN_PASSWORD_LENGTH = 8
    MAX_PASSWORD_LENGTH = 32