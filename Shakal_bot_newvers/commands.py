from utils import get_last_feed_time, update_weight, get_weight, get_relax_time, update_relax
import random
import time
from config import chat_states, chat_chance

async def handle_shakal_command(message):
    chat_id = message.chat.id
    chat_states[chat_id] = True
    chat_chance[chat_id] = 1
    await message.answer("Здарова, чё хотел?")

async def handle_shakalnost_command(message):
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

async def handle_feed_shakal(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.username

    # Получаем время последнего кормления
    last_feed = get_last_feed_time(chat_id, user_id)
    current_time = time.time()

    # Проверяем, прошло ли достаточно времени для кормления
    time_diff = current_time - last_feed
    if time_diff < 21600:
        remaining_time = 21600 - time_diff
        hours = int(remaining_time // 3600)
        minutes = int((remaining_time % 3600) // 60)
        await message.reply(f"Ты уже кормил шакала! Подожди ещё {hours} часов и {minutes} минут.")
        return

    # Генерация случайного набора веса
    weight_gain = round(random.uniform(0.1, 2), 1)

    # Обновляем вес шакала и время последнего кормления
    update_weight(chat_id, user_id, weight_gain, user_name)

    # Получаем новый вес после кормления
    new_weight = get_weight(chat_id, user_id)
    new_weight = round(new_weight, 1)

    await message.reply(f"Ты покормил шакала! Он набрал {weight_gain} кг. Теперь его вес {new_weight} кг.")


async def relaxshakal_handler(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    try:
        # Убираем распаковку, так как update_relax возвращает только одно значение (True или False)
        can_feed = update_relax(chat_id, user_id)
    except Exception as e:
        print(f"Произошла ошибка при обновлении. Ошибка: {str(e)}")  # Печать ошибки в консоль
        await message.reply("Произошла ошибка при обновлении. Попробуй снова.")
        return

    if can_feed:
        # Обновляем время последнего кормления, если можно кормить
        update_weight(chat_id, user_id, 0)  # Это обновит время кормления

        await message.reply("Ты обновил возможность кормить шакала снова! Можешь кормить его.")
    else:
        try:
            last_relax_time = await get_relax_time(chat_id, user_id)
        except Exception as e:
            print(f"Не удалось получить информацию о времени последнего обновления. Ошибка: {str(e)}")  # Печать ошибки в консоль
            await message.reply("Не удалось получить информацию о времени последнего обновления.")
            return

        current_time = time.time()
        remaining_time = max(0, 86400 - (current_time - last_relax_time))  # Защита от отрицательного времени

        hours = int(remaining_time // 3600)
        minutes = int((remaining_time % 3600) // 60)

        # Обработаем случай, когда время ожидания меньше минуты.
        if remaining_time < 60:
            await message.reply("Ты уже обновил возможность кормёжки. Подожди ещё меньше минуты.")
        else:
            await message.reply(f"Ты уже обновил возможность кормёжки. Подожди ещё {hours} часов и {minutes} минут.")
