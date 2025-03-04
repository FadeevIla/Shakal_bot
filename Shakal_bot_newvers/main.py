from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, BotCommand
from aiogram.filters import Command
import asyncio
import re
import random
import pymorphy2
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

TOKEN = "7554051873:AAGHIot1-qFu7or0RGTsTBslF6Mitnid95k"

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
morph = pymorphy2.MorphAnalyzer()

# Хранение состояния работы бота (отвечает или нет) для каждого чата
chat_states = {}
chat_chance = {}  # Вероятность ответа в процентах (по умолчанию 100%)

# Список триггеров
TRIGGERS = [
    (re.compile(r'^к[оа]роч[ье]?$', re.I), 'У кого короче, тот дома сидит!'),
    (re.compile(r'^нет$', re.I), 'Пидора ответ!'),
    (re.compile(r'^хо(чу|тим|тят|тел|тела)$', re.I), 'Хотеть невредно!'),
]

ANSWER_TO_QUESTION = "А тебя ебёт?"
QUESTION_WORDS = ["когда", "где", "почему", "зачем", "как", "сколько", "что", "кто"]

VOWEL_TO_RHYME = {"а": "я", "о": "ё", "у": "ю", "е": "е", "ы": "и", "и": "и", "э": "е", "ю": "ю", "я": "я"}
VOWELS = "аоуыэеёиюя"


def get_words(text):
    return re.findall(r'\b\w+\b', text.lower())


def get_by_word_trigger(text):
    for word in get_words(text):
        for pattern, response in TRIGGERS:
            if pattern.match(word):
                return response
    return None


def get_answer_to_question(text):
    if text.strip().endswith("?") or any(qw in text.lower() for qw in QUESTION_WORDS):
        return ANSWER_TO_QUESTION
    return None


def get_first_syllable(word):
    syllable = ""
    for letter in word:
        syllable += letter
        if letter in VOWELS:
            break
    return syllable


def get_rhyme(word):
    parsed = morph.parse(word)[0]
    if "NOUN" not in parsed.tag and "ADJF" not in parsed.tag:
        return None

    syllable = get_first_syllable(word)
    if not syllable or syllable == word:
        return None

    new_vowel = VOWEL_TO_RHYME.get(syllable[-1], syllable[-1])
    return f"ху{new_vowel}{word[len(syllable):]}"


def get_rhymes(text):
    return [get_rhyme(word) for word in get_words(text) if get_rhyme(word)]


@dp.message(Command("start"))
async def start_command(message: Message):
    chat_id = message.chat.id
    chat_states[chat_id] = True  # Включаем бота по умолчанию
    chat_chance[chat_id] = 100  # По умолчанию шанс 100%
    await message.answer("Здарова, чё хотел?")


@dp.message(Command("chance"))
async def set_chance(message: Message):
    chat_id = message.chat.id
    args = message.text.split()

    if len(args) < 2 or not args[1].isdigit():
        await message.reply("Использование: <code>/chance 1-100</code>")
        return

    chance = int(args[1])
    if not 1 <= chance <= 100:
        await message.reply("Укажи число от 1 до 100!")
        return

    chat_chance[chat_id] = chance
    await message.reply(f"Шанс ответа установлен на <b>{chance}%</b>!")


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
        return  # Если нет текста, игнорируем сообщение

    text = message.text.strip().lower()

    # Игнорируем команды, адресованные другим ботам
    if text.startswith("/") and "@" in text:
        return

    # Игнорируем любые команды, кроме известных боту
    if text.startswith("/") and text.split()[0] not in ["/chance", "/start"]:
        return

    if not chat_states.get(chat_id, True):
        return

    # Проверяем шанс ответа
    chance = chat_chance.get(chat_id, 100)
    if random.randint(1, 100) > chance:
        return

    # Проверяем разные типы ответа
    response = get_by_word_trigger(text) or get_answer_to_question(text) or (get_rhymes(text) or [None])[0]

    if not response:
        response = random.choice(["Чё?", "Ты базар фильтруй!", "Повтори, не понял!"])

    await message.reply(response)

async def set_bot_commands():
    commands = [
        BotCommand(command="start", description="Запуск бота"),
        BotCommand(command="chance", description="Установить шанс ответа (1-100)"),
    ]
    await bot.set_my_commands(commands)

async def main():
    print("Бот запущен!")
    await set_bot_commands()  # Устанавливаем команды
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
