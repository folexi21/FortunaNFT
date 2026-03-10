 import os
import asyncio
import json
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

TOKEN = os.environ.get("TOKEN")  # В переменные окружения добавьте ваш токен
bot = Bot(token=TOKEN)
dp = Dispatcher()

DATA_FILE = "users_data.json"

# Загрузка или создание базы пользователей
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        users = json.load(f)
else:
    users = {}

def save_users():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

# Призы с шансами
prizes = [
    ("50⭐", 40),
    ("100⭐", 30),
    ("500⭐", 20),
    ("🎨 NFT", 10)
]

def spin_wheel():
    rnd = random.randint(1, 100)
    acc = 0
    for prize, chance in prizes:
        acc += chance
        if rnd <= acc:
            return prize
    return prizes[0][0]

# Главное меню
def main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🎰 Крутить рулетку", callback_data="open_roulette"),
                InlineKeyboardButton(text="💰 Мой баланс", callback_data="balance")
            ],
            [
                InlineKeyboardButton(text="🏆 Мои призы", callback_data="prizes"),
                InlineKeyboardButton(text="💳 Пополнить ⭐", callback_data="add_stars")
            ],
            [
                InlineKeyboardButton(text="🛠 Модерация", callback_data="moderation")
            ]
        ]
    )

# Меню рулетки
def roulette_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔄 Прокрутить ещё раз", callback_data="roulette"),
                InlineKeyboardButton(text="⬅ Главное меню", callback_data="main_menu")
            ]
        ]
    )

# /start
@dp.message()
async def start(message: types.Message):
    user_id = str(message.from_user.id)
    users.setdefault(user_id, {"balance": 100, "prizes": []})
    save_users()
    await message.answer(
        "🎉 Добро пожаловать в FortunaNFT!\n"
        "✨ Испытай удачу и собирай редкие NFT и звезды!\n"
        "💡 Совет: начинайте с прокрутки рулетки, чтобы выигрывать призы!",
        reply_markup=main_menu()
    )

# Обработка нажатий кнопок
@dp.callback_query()
async def handle_buttons(callback: types.CallbackQuery):
    user_id = str(callback.from_user.id)
    users.setdefault(user_id, {"balance": 100, "prizes": []})
    user = users[user_id]
    data = callback.data

    if data == "open_roulette":
        await callback.message.answer(
            "🎰 Добро пожаловать в меню рулетки! Каждый спин стоит 30⭐",
            reply_markup=roulette_menu()
        )

    elif data == "roulette":
        if user["balance"] < 30:
            await callback.message.answer("⚠ У вас недостаточно ⭐ для прокрутки. Пополните баланс!")
            return

        # Списание 30 звезд
        user["balance"] -= 30
        save_users()

        wheel_options = ["50⭐", "100⭐", "500⭐", "🎨 NFT"]
        # Анимация прокрутки
        for _ in range(5):
            await callback.message.answer(f"🎡 {random.choice(wheel_options)} …")
            await asyncio.sleep(0.5)

        final_prize = spin_wheel()
        user["prizes"].append(final_prize)
        save_users()
        await callback.message.answer(
            f"🏆 ФИНАЛ: Вы выиграли {final_prize}!\n"
            "Призы будут выданы на ваш аккаунт в течение 3 дней.",
            reply_markup=roulette_menu()
        )

    elif data == "balance":
        await callback.message.answer(f"💎 Ваш баланс: {user['balance']} ⭐")

    elif data == "prizes":
        if user["prizes"]:
            await callback.message.answer("🏅 Ваши призы:\n" + "\n".join(user["prizes"]))
        else:
            await callback.message.answer("😔 У вас пока нет призов.")

    elif data == "add_stars":
        user["balance"] += 100
        save_users()
        await callback.message.answer("💰 Ваш баланс увеличен на 100 ⭐!")

    elif data == "moderation":
        await callback.message.answer("Свяжитесь с модерацией: @ronaldureal")

    elif data == "main_menu":
        await callback.message.answer("⬅ Вы вернулись в главное меню", reply_markup=main_menu())

# Запуск бота
if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
