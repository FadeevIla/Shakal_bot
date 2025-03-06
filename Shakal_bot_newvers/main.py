import asyncio
from config import bot, dp
from handlers import dp
from aiogram.types import Message, BotCommand

async def set_bot_commands():
    commands = [
        BotCommand(command="shakal", description="Запуск бота"),
        BotCommand(command="shakalnost", description="Установить шанс ответа (1-100)"),
        BotCommand(command="shakalvoice", description="Случайная цитата"),
    ]
    await bot.set_my_commands(commands)


async def main():
    print("Бот запущен!")
    await set_bot_commands()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
