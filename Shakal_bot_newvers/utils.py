import re
import random
from pymystem3 import Mystem
import json
import os
import time
from config import bot

DATA_FILE = "shakal_weight.json"
FEED_COOLDOWN = 3600  # 1 час в секундах

mystem = Mystem()

TRIGGERS = [
    (re.compile(r'^к[оа]роч[ье]?$', re.I), 'У кого короче, тот дома сидит!'),
    (re.compile(r'^нет$', re.I), 'Пидора ответ!'),
    (re.compile(r'^хо(чу|тим|тят|тел|тела)$', re.I), 'Хотеть невредно!'),
]

ANSWER_TO_QUESTION = "А тебя ебёт?"
QUESTION_WORDS = ["когда", "где", "почему", "зачем", "как", "сколько", "что", "кто"]

def get_words(text):
    """ Разбивает текст на слова """
    return re.findall(r'\b\w+\b', text.lower())

def get_by_word_trigger(text):
    """ Проверяет текст на соответствие триггерам """
    for word in get_words(text):
        for pattern, response in TRIGGERS:
            if pattern.match(word):
                return response
    return None

def get_answer_to_question(text):
    """ Проверяет, является ли текст вопросом """
    if text.strip().endswith("?") or any(qw in text.lower() for qw in QUESTION_WORDS):
        return ANSWER_TO_QUESTION
    return None

# Проверка, существует ли файл данных
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}


# Функция для записи данных в JSON (с округлением)
def save_data(data):
    # Округление весов до 1 знака после запятой
    for chat_id, users in data.items():
        for user_id, user_data in users.items():
            user_data["weight"] = round(user_data["weight"], 1)

    # Запись данных в JSON
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Функция для получения веса шакала
def get_weight(chat_id, user_id):
    data = load_data()
    user_data = data.get(str(chat_id), {}).get(str(user_id), {})
    return user_data.get("weight", 0)

# Функция для обновления веса шакала
def update_weight(chat_id, user_id, weight_change, user_name=None, update_feed_time=True):
    data = load_data()
    if str(chat_id) not in data:
        data[str(chat_id)] = {}
    if str(user_id) not in data[str(chat_id)]:
        data[str(chat_id)][str(user_id)] = {"weight": 0, "last_feed_time": 0,
                                            "username": user_name}  # Добавляем имя пользователя

    current_weight = data[str(chat_id)][str(user_id)].get("weight", 0)
    new_weight = current_weight + weight_change

    # Обновляем вес пользователя
    data[str(chat_id)][str(user_id)]["weight"] = new_weight

    # Обновляем время кормления только если нужно
    if update_feed_time:
        data[str(chat_id)][str(user_id)]["last_feed_time"] = time.time()  # Устанавливаем текущее время

    save_data(data)


# Функция для получения имени пользователя через API
async def get_user_name_from_api(chat_id, user_id):
    """Функция для получения имени пользователя через API, если его нет в данных."""
    try:
        user = await bot.get_chat_member(chat_id, user_id)
        return user.user.full_name  # Можно использовать user.user.username для получения username
    except Exception as e:
        print(f"Ошибка при получении имени пользователя: {e}")
        return "Неизвестный пользователь"

# Функция для получения топа пользователей по весу
async def get_top(chat_id, top_n=5):
    data = load_data()
    if str(chat_id) not in data or not data[str(chat_id)]:
        return ["Нет данных для показа топа."]

    users = data[str(chat_id)].items()
    sorted_users = sorted(users, key=lambda x: x[1].get("weight", 0), reverse=True)

    # Для каждого пользователя добавим имя (можно сохранить имя при кормлении или получить как-то иначе)
    top_users = []
    for user_id, user_data in sorted_users[:top_n]:
        # Попытка получить имя из данных, если оно отсутствует — получаем через API
        user_name = user_data.get("username", await get_user_name_from_api(chat_id, user_id))
        weight = user_data["weight"]
        # Собираем информацию в словарь
        top_users.append({"id": user_id, "name": user_name, "weight": weight})

    return top_users

# Функция для получения времени последнего кормления
def get_last_feed_time(chat_id, user_id):
    data = load_data()
    user_data = data.get(str(chat_id), {}).get(str(user_id), {})
    return user_data.get("last_feed_time", 0)  # Возвращаем 0, если нет времени кормления

# Функция для обновления времени последнего кормления
def update_relax(chat_id, user_id):
    try:
        data = load_data()  # Попробуем загрузить данные
    except Exception as e:
        print(f"Ошибка при загрузке данных: {str(e)}")
        return False  # Возвращаем False в случае ошибки загрузки данных

    # Обрабатываем структуру данных (создаём нужные ключи, если их нет)
    if str(chat_id) not in data:
        data[str(chat_id)] = {}
    if str(user_id) not in data[str(chat_id)]:
        data[str(chat_id)][str(user_id)] = {"weight": 0, "last_feed_time": 0, "relax_time": 0}  # Добавляем relax_time

    current_time = time.time()
    last_relax_time = data[str(chat_id)][str(user_id)].get("relax_time", 0)

    # Проверяем, прошло ли 24 часа
    if current_time - last_relax_time >= 86400:  # 86400 секунд = 24 часа
        # Обновляем relax_time
        data[str(chat_id)][str(user_id)]["relax_time"] = current_time
        # Обновляем last_feed_time, чтобы можно было сразу кормить
        data[str(chat_id)][str(user_id)]["last_feed_time"] = current_time

        try:
            save_data(data)  # Попробуем сохранить данные
        except Exception as e:
            print(f"Ошибка при сохранении данных: {str(e)}")
            return False  # Возвращаем False, если не удалось сохранить данные

        return True  # Возвращаем True, если можно кормить снова
    else:
        return False  # Возвращаем False, если нужно подождать

# Функция для получения времени последнего обновления возможности кормёжки
def get_relax_time(chat_id, user_id):
    data = load_data()
    user_data = data.get(str(chat_id), {}).get(str(user_id), {})
    return user_data.get("last_relax_time", 0)

# Функция для обновления времени последнего обновления возможности кормёжки
def update_relax(chat_id, user_id):
    data = load_data()

    if str(chat_id) not in data:
        data[str(chat_id)] = {}
    if str(user_id) not in data[str(chat_id)]:
        data[str(chat_id)][str(user_id)] = {"weight": 0, "last_feed_time": 0, "relax_time": 0}  # Relax time added

    current_time = time.time()
    last_relax_time = data[str(chat_id)][str(user_id)].get("relax_time", 0)

    # Check if 24 hours have passed since the last relaxation
    if current_time - last_relax_time >= 86400:  # 86400 seconds = 24 hours
        # Update relax_time and return True (user can feed again)
        data[str(chat_id)][str(user_id)]["relax_time"] = current_time
        save_data(data)
        return True
    else:
        # Calculate the remaining time until the next relaxation update
        remaining_time = 86400 - (current_time - last_relax_time)
        hours = int(remaining_time // 3600)
        minutes = int((remaining_time % 3600) // 60)
        return False, hours, minutes  # Return False and time remaining for feedback
