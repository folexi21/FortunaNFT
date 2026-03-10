import random
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import os

# Токен из переменных среды
TOKEN = os.environ.get("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(KeyboardButton("🎰 Крутить рулетку"))
menu.add(KeyboardButton("💰 Мой баланс"), KeyboardButton("📊 Шансы"))
menu.add(KeyboardButton("🏆 Мои призы"), KeyboardButton("🛠 Модерация"))

users_data = {}  # {user_id: {"stars": int, "prizes": []}}

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    uid = message.from_user.id
    if uid not in users_data:
        users_data[uid] = {"stars": 100, "prizes": []}

    balance = users_data[uid]["stars"]
    text = f"""
🎰 FortunaNFT

💰 Твой баланс: {balance} ⭐

Испытай удачу!

💸 Цена прокрутки: 30 ⭐
"""
    await message.answer(text, reply_markup=menu)

@dp.message_handler(lambda m: m.text == "💰 Мой баланс")
async def show_balance(message: types.Message):
    uid = message.from_user.id
    bal = users_data.get(uid, {}).get("stars", 0)
    await message.answer(f"💰 Баланс: {bal} ⭐")

@dp.message_handler(lambda m: m.text == "📊 Шансы")
async def chances(message: types.Message):
    text = """
📊 Шансы выпадения призов:

❌ Ничего — 60%
⭐ 50 Stars — 20%
⭐ 100 Stars — 12%
⭐ 500 Stars — 6%
💎 NFT — 2%

Цена: 30 ⭐
"""
    await message.answer(text)

@dp.message_handler(lambda m: m.text == "🎰 Крутить рулетку")
async def spin(message: types.Message):
    uid = message.from_user.id
    user = users_data.get(uid)

    if user["stars"] < 30:
        await message.answer("❌ Недостаточно ⭐ для прокрутки.")
        return

    user["stars"] -= 30

    number = random.randint(1, 100)
    if number <= 60:
        res = "😢 Ничего не выпало."
    elif number <= 80:
        res = "🎉 Ты выиграл 50 ⭐!"
        user["stars"] += 50
    elif number <= 92:
        res = "🔥 Ты выиграл 100 ⭐!"
        user["stars"] += 100
    elif number <= 98:
        res = "💰 JACKPOT! Ты выиграл 500 ⭐!"
        user["stars"] += 500
    else:
        res = "💎 Ура! Ты выиграл NFT!"

    user["prizes"].append(res)
    await message.answer("🎰 Крутим рулетку...")
    await message.answer(res)

@dp.message_handler(lambda m: m.text == "🏆 Мои призы")
async def show_prizes(message: types.Message):
    uid = message.from_user.id
    prizes = users_data.get(uid, {}).get("prizes", [])
    if not prizes:
        await message.answer("🏆 Пока нет призов.")
    else:
        await message.answer("🏆 Твои призы:\n" + "\n".join(prizes))

@dp.message_handler(lambda m: m.text == "🛠 Модерация")
async def support(message: types.Message):
    await message.answer("🛠 Связь с модерацией: @ronaldureal")

if __name__ == "__main__":
    executor.start_polling(dp)