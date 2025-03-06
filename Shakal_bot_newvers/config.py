from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

TOKEN = "7554051873:AAGHIot1-qFu7or0RGTsTBslF6Mitnid95k"

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Состояние бота в чатах
chat_states = {}
chat_chance = {}  # Шанс ответа в процентах (по умолчанию 100%)
