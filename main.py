import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardButton
import asyncio

BOT_TOKEN = "8710709672:AAHov0L0RHWeXOVBY3wnpIxk25-aL08g_rE"  # вставь свой токен

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Список NFT
nfts = [
    {"id": 1, "name": "Ramadan NFT", "image": "https://i.imgur.com/1.png", "original_price": 100},
    {"id": 2, "name": "UFC NFT", "image": "https://i.imgur.com/2.png", "original_price": 150},
    {"id": 3, "name": "SnubDoc NFT", "image": "https://i.imgur.com/3.png", "original_price": 120},
    {"id": 4, "name": "CryptoPunk NFT", "image": "https://i.imgur.com/4.png", "original_price": 200},
    {"id": 5, "name": "BoredApe NFT", "image": "https://i.imgur.com/5.png", "original_price": 250},
    {"id": 6, "name": "Azuki NFT", "image": "https://i.imgur.com/6.png", "original_price": 180},
    {"id": 7, "name": "CloneX NFT", "image": "https://i.imgur.com/7.png", "original_price": 220},
    {"id": 8, "name": "Meebits NFT", "image": "https://i.imgur.com/8.png", "original_price": 140},
    {"id": 9, "name": "Moonbirds NFT", "image": "https://i.imgur.com/9.png", "original_price": 160},
    {"id": 10, "name": "PudgyPenguins NFT", "image": "https://i.imgur.com/10.png", "original_price": 130},
    {"id": 11, "name": "VeeFriends NFT", "image": "https://i.imgur.com/11.png", "original_price": 170},
    {"id": 12, "name": "World of Women NFT", "image": "https://i.imgur.com/12.png", "original_price": 210},
    {"id": 13, "name": "Azrael NFT", "image": "https://i.imgur.com/13.png", "original_price": 190},
    {"id": 14, "name": "CyberKongz NFT", "image": "https://i.imgur.com/14.png", "original_price": 180},
    {"id": 15, "name": "RTFKT NFT", "image": "https://i.imgur.com/15.png", "original_price": 230},
]

# Клавиатура магазина
def shop_menu():
    builder = InlineKeyboardBuilder()
    for nft in nfts:
        price = int(nft["original_price"] * 0.8)  # 20% скидка
        builder.button(
            text=f"{nft['name']} ⭐{price}",
            callback_data=f"nft_{nft['id']}"
        )
    builder.adjust(2)
    return builder.as_markup()

# Кнопки действий NFT
def nft_actions(nft_id):
    nft = next((x for x in nfts if x["id"] == nft_id), None)
    if nft is None:
        return InlineKeyboardBuilder().as_markup()
    price = int(nft["original_price"] * 0.8)
    builder = InlineKeyboardBuilder()
    builder.button(
        text=f"💬 Contact Seller (@ronaldureal) ⭐{price}",
        url="https://t.me/ronaldureal"
    )
    builder.button(
        text="⬅ Back to Shop",
        callback_data="back_shop"
    )
    builder.adjust(1)
    return builder.as_markup()

# /start
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "🎉 Привет! Добро пожаловать в FortunaNFT 🎨\n\n"
        "Здесь ты можешь выбрать NFT и купить его со скидкой 20%.\n"
        "Нажми на понравившийся NFT ниже, чтобы узнать подробнее!",
        reply_markup=shop_menu()
    )

# Обработка нажатий
@dp.callback_query()
async def callback_handler(callback: types.CallbackQuery):
    data = callback.data
    if data.startswith("nft_"):
        nft_id = int(data.split("_")[1])
        nft = next((x for x in nfts if x["id"] == nft_id), None)
        if nft:
            await callback.message.answer_photo(
                nft["image"],
                caption=f"{nft['name']}\nОригинальная цена: {nft['original_price']} ⭐\nСкидка 20%!",
                reply_markup=nft_actions(nft_id)
            )
    elif data == "back_shop":
        await callback.message.answer(
            "🛒 Возврат в магазин NFT:",
            reply_markup=shop_menu()
        )

# Запуск
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
