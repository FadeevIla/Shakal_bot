from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()  # Загружаем переменные из .env
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("Токен не найден в .env файле!")

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Состояние бота в чатах
chat_states = {}
chat_chance = {}  # Шанс ответа в процентах (по умолчанию 100%)

async def on_shutdown(dp):
    """Корректное завершение работы бота и закрытие соединений."""
    await bot.close()  # Закрыть сессию бота
    await dp.storage.close()  # Закрыть хранилище
    await dp.storage.wait_closed()  # Дождаться завершения всех операций с хранилищем
