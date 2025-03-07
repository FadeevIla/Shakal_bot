import asyncio
from config import bot, dp
import handlers
from aiogram.types import BotCommand, BotCommandScopeDefault
import aiogram



async def set_bot_commands():
    commands = [
        BotCommand(command="shakal", description="Запуск бота"),
        BotCommand(command="shakalnost", description="Установить шанс ответа (1-100)"),
        BotCommand(command="shakalvoice", description="Случайная цитата"),
        BotCommand(command="feedshakal", description="Покормить шакала"),
        BotCommand(command="fightshakal", description="Дуэль на вес"),
        BotCommand(command="topshakal", description="Топ игроков по весу"),
  #      BotCommand(command="relaxshakal", description="Отдохнуть шакалу"),
    ]
    #print("Setting bot commands:", commands)  # Логирование
    try:
        await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
    except aiogram.exceptions.TelegramBadRequest as e:
        print(f"Ошибка при установке команд: {e}")


async def main():
    print("Бот запущен!")
    await set_bot_commands()

    # Запуск polling для обработки сообщений
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
