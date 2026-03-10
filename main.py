import os
import asyncio
import json
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random

TOKEN = os.environ.get("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

DATA_FILE = "users_data.json"

# Загрузка данных
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        users = json.load(f)
else:
    users = {}

def save_users():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

# Инлайн меню
def get_menu():
    menu = InlineKeyboardMarkup(row_width=2)
    menu.add(
        InlineKeyboardButton("🎰 Крутить рулетку", callback_data="roulette"),
        InlineKeyboardButton("💰 Мой баланс", callback_data="balance"),
        InlineKeyboardButton("🏆 Мои призы", callback_data="prizes"),
        InlineKeyboardButton("💳 Пополнить звезды", callback_data="add_stars"),
        InlineKeyboardButton("🛠 Модерация", callback_data="moderation")
    )
    return menu

# Призы с шансами
prizes = [
    ("50⭐", 40),    # 40% шанс
    ("100⭐", 30),   # 30% шанс
    ("500⭐", 20),   # 20% шанс
    ("🎨 NFT", 10)   # 10% шанс
]

def spin_wheel():
    rnd = random.randint(1, 100)
    acc = 0
    for prize, chance in prizes:
        acc += chance
        if rnd <= acc:
            return prize
    return prizes[0][0]  # на всякий случай

# /start
@dp.message()
async def start(message: types.Message):
    user_id = str(message.from_user.id)
    users.setdefault(user_id, {"balance": 100, "prizes": []})
    save_users()
    await message.answer(
        "🎉 Добро пожаловать в FortunaNFT!\n"
        "✨ Испытай удачу, собирай звезды и редкие NFT!\n"
        "⚡ Сегодня твой день — крути и выигрывай!",
        reply_markup=get_menu()
    )

# Обработка нажатий
@dp.callback_query()
async def handle_buttons(callback: types.CallbackQuery):
    user_id = str(callback.from_user.id)
    users.setdefault(user_id, {"balance": 100, "prizes": []})
    user = users[user_id]
    data = callback.data

    if data == "roulette":
        if user["balance"] < 30:
            await callback.message.answer("⚠ У вас недостаточно ⭐ для прокрутки.")
            return
        user["balance"] -= 30
        save_users()

        # Анимация рулетки
        wheel_options = ["50⭐", "100⭐", "500⭐", "🎨 NFT"]
        spin_messages = random.choices(wheel_options, k=5)  # 5 итераций
        for option in spin_messages:
            await callback.message.answer(f"🎡 {option} …")
            await asyncio.sleep(0.5)

        final_prize = spin_wheel()
        user["prizes"].append(final_prize)
        save_users()
        await callback.message.answer(
            f"🏆 ФИНАЛ: Вы выиграли {final_prize}!\n"
            "Призы будут выданы на ваш аккаунт в течение 3 дней."
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

# Запуск
if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
