import os
import asyncio
import json
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import random

# Токен
TOKEN = os.environ.get("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Файл для хранения данных пользователей
DATA_FILE = "users_data.json"

# Загружаем данные, если файл есть
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        users = json.load(f)
else:
    users = {}

# Сохраняем данные в файл
def save_users():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

# Меню
menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("🎰 Крутить рулетку"), KeyboardButton("💰 Мой баланс")],
        [KeyboardButton("🏆 Мои призы"), KeyboardButton("💳 Пополнить звезды")],
        [KeyboardButton("🛠 Модерация")]
    ],
    resize_keyboard=True
)

# /start
@dp.message()
async def start(message: types.Message):
    user_id = str(message.from_user.id)
    users.setdefault(user_id, {"balance": 100, "prizes": []})
    save_users()
    await message.answer(
        "🎉 Привет! Добро пожаловать в FortunaNFT 🎰\n\n"
        "Каждая прокрутка рулетки стоит 30 ⭐.\n"
        "Призы будут выданы на ваш аккаунт в течение 3 дней.",
        reply_markup=menu
    )

# Обработка кнопок
@dp.message()
async def handle_buttons(message: types.Message):
    user_id = str(message.from_user.id)
    users.setdefault(user_id, {"balance": 100, "prizes": []})
    user = users[user_id]

    text = message.text

    if text == "🎰 Крутить рулетку":
        if user["balance"] < 30:
            await message.answer("⚠ У вас недостаточно ⭐ для прокрутки.")
            return
        user["balance"] -= 30
        prize = random.choice(["50⭐", "100⭐", "500⭐", "🎨 NFT"])
        user["prizes"].append(prize)
        save_users()
        await message.answer(
            f"🎁 Поздравляем! Вы выиграли {prize}\n"
            "Призы будут выданы на ваш аккаунт в течение 3 дней."
        )

    elif text == "💰 Мой баланс":
        await message.answer(f"💎 Ваш баланс: {user['balance']} ⭐")

    elif text == "🏆 Мои призы":
        if user["prizes"]:
            await message.answer("🏅 Ваши призы:\n" + "\n".join(user["prizes"]))
        else:
            await message.answer("😔 У вас пока нет призов.")

    elif text == "💳 Пополнить звезды":
        user["balance"] += 100
        save_users()
        await message.answer("💰 Ваш баланс увеличен на 100 ⭐!")

    elif text == "🛠 Модерация":
        await message.answer("Свяжитесь с модерацией: @ronaldureal")

# Запуск бота
if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))