#handlers.py

from aiogram import Dispatcher, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import F
from config import bot, chat_states, chat_chance, dp
from quotes import generate_quote
from commands import handle_shakal_command, handle_shakalnost_command, handle_feed_shakal, relaxshakal_handler
from battle import fight_shakal, accept_fight, decline_fight
from utils import get_top, get_by_word_trigger, get_answer_to_question

@dp.message(Command("shakal"))
async def shakal_command(message: Message):
    await handle_shakal_command(message)

@dp.message(Command("shakalnost"))
async def shakalnost_command(message: Message):
    await handle_shakalnost_command(message)

@dp.message(Command("shakalvoice"))
async def send_shakal_wisdom(message: Message):
    quote = generate_quote()
    await message.answer(quote)

@dp.message(F.text.lower() == "шакал, цитата")
async def send_shakal_wisdom(message: Message):
    quote = generate_quote()
    await message.answer(quote)

@dp.message(F.text.lower() == "шакал, включись")
async def enable_bot(message: Message):
    chat_states[message.chat.id] = True
    await message.answer("Я тут, базарю!")

@dp.message(F.text.lower() == "шакал, отключись")
async def disable_bot(message: Message):
    chat_states[message.chat.id] = False
    await message.answer("Захлопнись!")

@dp.message(Command("fightshakal"))
async def start_duel(message: Message):
    await fight_shakal(message)

@dp.callback_query(lambda c: c.data.startswith("accept_fight_"))
async def accept_duel(callback_query: CallbackQuery):
    await accept_fight(callback_query)

@dp.callback_query(lambda c: c.data.startswith("decline_fight_"))
async def decline_duel(callback_query: CallbackQuery):
    await decline_fight(callback_query)

@dp.message(Command("feedshakal"))
async def feed_shakal(message: Message):
    await handle_feed_shakal(message)

@dp.message(Command("relaxshakal"))
async def relax_shakal(message: Message):
    await relaxshakal_handler(message)

@dp.message(Command("topshakal"))
async def show_top(message: Message):
    leaderboard = await get_top(message.chat.id)  # Добавить await
    # Преобразуем список в строку, чтобы передать его в message.answer
    leaderboard_text = "\n".join([f"{user['name']}: {user['weight']} кг" for user in leaderboard])
    await message.answer(f"Топ пользователей:\n{leaderboard_text}")


@dp.message(F.text.lower().startswith("фас "))
async def duel_by_text(message: Message):
    await fight_shakal(message)

@dp.message(F.text)
async def handle_text_messages(message: Message):
    text = message.text
    print(f"Получено сообщение: {text}")  # Логирование для отладки

    # Проверка на триггеры
    trigger_response = get_by_word_trigger(text)
    if trigger_response:
        print(f"Сработал триггер: {trigger_response}")  # Логирование
        await message.reply(trigger_response)
        return

    # Проверка на вопрос
    question_response = get_answer_to_question(text)
    if question_response:
        print(f"Сработал ответ на вопрос: {question_response}")  # Логирование
        await message.reply(question_response)
        return

