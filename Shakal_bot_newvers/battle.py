# battle.py:
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from utils import get_weight, update_weight, get_top
import random
from config import bot

async def get_user_name(chat_id: int, user_id: int) -> str:
    """Функция для получения имени пользователя по ID."""
    try:
        user = await bot.get_chat_member(chat_id, user_id)
        return user.user.full_name  # Можно также использовать user.user.username для username
    except Exception as e:
        print(f"Ошибка при получении имени пользователя: {e}")
        return "Неизвестный"

async def fight_shakal(message: Message):
    """Команда для дуэли шакалов с кнопками подтверждения/отказа."""
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    args = message.text.split()

    if len(args) < 2:
        await message.reply("⚔ Использование: <code>/fight СТАВКА</code>")
        return

    try:
        bet = float(args[1])
        if bet <= 0:
            raise ValueError
    except ValueError:
        await message.reply("⚠ Введите корректное число больше 0.")
        return

    current_weight = get_weight(chat_id, user_id)

    if current_weight < bet:
        await message.reply(f"❌ У шакала {user_name} нет столько веса! (Ваш вес: {current_weight} кг)")
        return

    if message.reply_to_message:
        opponent_id = message.reply_to_message.from_user.id
        opponent_name = message.reply_to_message.from_user.first_name

        if opponent_id == user_id:
            await message.reply("❌ Вы не можете сразиться с самим собой!")
            return

        opponent_weight = get_weight(chat_id, opponent_id)

        if opponent_weight < bet:
            await message.reply(f"❌ У противника {opponent_name} недостаточно веса для ставки!")
            return

        callback_data_accept = f"accept_fight_{user_id}_{opponent_id}_{bet}"
        callback_data_decline = f"decline_fight_{user_id}"

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Принять", callback_data=callback_data_accept)],
            [InlineKeyboardButton(text="Отказаться", callback_data=callback_data_decline)]
        ])

        await message.answer(
            f"🔥 Дуэль между шакалами!\n"
            f"⚔ {user_name} VS {opponent_name}\n"
            f"🏆 Ставка: {bet} кг\n\n"
            f"Вы хотите принять дуэль?",
            reply_markup=keyboard
        )

    else:
        await message.reply("❌ Чтобы вызвать дуэль, ответьте на сообщение другого игрока.")

async def accept_fight(callback_query: CallbackQuery):
    """Обработка принятия дуэли."""
    print(f"DEBUG: Callback data = {callback_query.data}")  # Логируем полученные данные

    try:
        parts = callback_query.data.split('_')  # Разбиваем данные
        print(f"DEBUG: len(parts) = {len(parts)}, parts = {parts}")  # Логируем результат split

        if len(parts) != 5 or parts[0] != "accept" or parts[1] != "fight":
            raise ValueError("Неверный формат данных")

        user_id = int(parts[2])
        opponent_id = int(parts[3])
        bet = round(float(parts[4]), 1)  # Округляем ставку до 1 знака после запятой
    except (ValueError, IndexError) as e:
        print(f"ERROR: {e}")  # Логируем ошибку
        await callback_query.answer("❌ Ошибка в данных дуэли.", show_alert=True)
        return

    chat_id = callback_query.message.chat.id
    from_user_id = callback_query.from_user.id

    if from_user_id != opponent_id:
        await callback_query.answer("❌ Вы не можете принимать эту дуэль!", show_alert=True)
        return

    user_name = callback_query.from_user.first_name
    opponent_name = await get_user_name(chat_id, user_id)

    current_weight = get_weight(chat_id, from_user_id)
    if current_weight < bet:
        await callback_query.message.answer(f"❌ {user_name}, у вас недостаточно веса для ставки!")
        return

    opponent_weight = get_weight(chat_id, user_id)
    if opponent_weight < bet:
        await callback_query.message.answer(f"❌ {opponent_name} не может участвовать — недостаточно веса!")
        return

    winner_id, loser_id = random.sample([user_id, opponent_id], 2)

    # Обновляем только вес, не изменяя времени кормления
    update_weight(chat_id, winner_id, bet, update_feed_time=False)
    update_weight(chat_id, loser_id, -bet, update_feed_time=False)

    winner_name = await get_user_name(chat_id, winner_id)
    loser_name = await get_user_name(chat_id, loser_id)

    # Получаем новый вес победителя
    winner_new_weight = round(get_weight(chat_id, winner_id), 1)

    await callback_query.message.answer(
        f"🔥 Дуэль завершена!\n"
        f"⚔ {user_name} VS {opponent_name}\n"
        f"🏆 Победил {winner_name} и забрал {bet} кг веса!\n"
        f"📊 Теперь его вес: {winner_new_weight} кг"
    )

    # Удаляем сообщение с кнопками
    await callback_query.message.delete()

async def decline_fight(callback_query: CallbackQuery):
    """Обработка отказа от дуэли."""
    try:
        data = callback_query.data.split('_')
        user_id = int(data[1])
    except (ValueError, IndexError):
        await callback_query.answer("❌ Ошибка в данных дуэли.", show_alert=True)
        return

    chat_id = callback_query.message.chat.id
    from_user_id = callback_query.from_user.id

    if from_user_id != user_id:
        await callback_query.answer("❌ Вы не можете отклонить эту дуэль!", show_alert=True)
        return

    await callback_query.message.answer("❌ Дуэль отклонена.")

    # Удаляем сообщение с кнопками
    await callback_query.message.delete()
