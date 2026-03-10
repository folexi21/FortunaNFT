import os
import json
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command
from aiogram import F

# Токен из переменной окружения на Railway
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Мини-база пользователей (в будущем можно заменить на файл или базу)
if os.path.exists("users.json"):
    with open("users.json", "r") as f:
        users = json.load(f)
else:
    users = {}

# Цены и призы
SPIN_COST = 30
PRIZES = ["50 ⭐", "100 ⭐", "500 ⭐", "Cheap NFT"]

# Создание меню
def get_menu():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🎰 Spin Roulette", callback_data="spin"),
        InlineKeyboardButton(text="💰 My Balance", callback_data="balance")
    )
    builder.row(
        InlineKeyboardButton(text="📞 Contact Support", url="https://t.me/ronaldureal")
    )
    return builder.as_markup()

# Проверка и создание пользователя
def check_user(user_id):
    if str(user_id) not in users:
        users[str(user_id)] = {"stars": 100}  # стартовый баланс
        save_users()

def save_users():
    with open("users.json", "w") as f:
        json.dump(users, f)

# Стартовое сообщение
@dp.message(Command("start"))
async def start(message: types.Message):
    check_user(message.from_user.id)
    await message.answer(
        f"🎉 Welcome to FortunaNFT!\n\n"
        f"Your adventure in NFT roulette begins here! 🃏\n"
        f"Press the buttons below to explore your luck!",
        reply_markup=get_menu()
    )

# Обработка нажатий на меню
@dp.callback_query(F.data == "spin")
async def spin_roulette(call: types.CallbackQuery):
    user_id = str(call.from_user.id)
    check_user(user_id)

    if users[user_id]["stars"] < SPIN_COST:
        await call.answer("❌ You don't have enough ⭐ to spin!", show_alert=True)
        return

    users[user_id]["stars"] -= SPIN_COST
    prize = random.choice(PRIZES)
    # Если приз это звезды, добавляем их
    if "⭐" in prize:
        stars_amount = int(prize.split()[0])
        users[user_id]["stars"] += stars_amount

    save_users()
    await call.message.edit_text(
        f"🎰 You spun the roulette!\n\nYou won: {prize}\n"
        f"Your current balance: {users[user_id]['stars']} ⭐",
        reply_markup=get_menu()
    )

@dp.callback_query(F.data == "balance")
async def show_balance(call: types.CallbackQuery):
    user_id = str(call.from_user.id)
    check_user(user_id)
    await call.message.edit_text(
        f"💰 Your balance: {users[user_id]['stars']} ⭐",
        reply_markup=get_menu()
    )

# Запуск бота
if __name__ == "__main__":
    import asyncio
    from aiogram import Bot, Dispatcher
    from aiogram.utils.platform import get_event_loop

    asyncio.run(dp.start_polling(bot))
