from aiogram import F
from aiogram.types import Message, BotCommand
from aiogram.filters import Command
import random
from config import bot, dp, chat_states, chat_chance
from utils import get_by_word_trigger, get_answer_to_question, get_rhymes
from quotes import generate_quote
from llama_chat import chat_with_llama


@dp.message(Command("shakal"))
async def shakal_command(message: Message):
    chat_id = message.chat.id
    chat_states[chat_id] = True
    chat_chance[chat_id] = 1
    await message.answer("Здарова, чё хотел?")


@dp.message(Command("shakalnost"))
async def shakalnost_command(message: Message):
    chat_id = message.chat.id
    args = message.text.split()

    if len(args) < 2 or not args[1].isdigit():
        await message.reply("Использование: <code>/shakalnost 1-100</code>")
        return

    chance = int(args[1])
    if not 1 <= chance <= 100:
        await message.reply("Укажи число от 1 до 100!")
        return

    chat_chance[chat_id] = chance
    await message.reply(f"Шанс ответа установлен на <b>{chance}%</b>!")


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
    await message.answer("Ладно, молчу.")


@dp.message()
async def handle_message(message: Message):
    chat_id = message.chat.id
    if not message.text:
        return

    text = message.text.strip().lower()
    if not chat_states.get(chat_id, True):
        return

    chance = chat_chance.get(chat_id, 100)
    if random.randint(1, 100) > chance:
        return

    response = get_by_word_trigger(text) or get_answer_to_question(text) or (get_rhymes(text) or [None])[0]
    if not response:
        return

    await message.reply(response)
