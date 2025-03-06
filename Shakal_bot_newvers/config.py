from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
import os

load_dotenv()  # Загружаем переменные из .env
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("Токен не найден в .env файле!")

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Состояние бота в чатах
chat_states = {}
chat_chance = {}  # Шанс ответа в процентах (по умолчанию 100%)
