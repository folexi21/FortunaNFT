import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio

BOT_TOKEN = "8710709672:AAHov0L0RHWeXOVBY3wnpIxk25-aL08g_rE"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Список NFT
nfts = [
    {"id": 1, "name": "Ramadan NFT", "image": "https://i.ibb.co/9p3cGZQ/ramadan.jpg", "original_price": 100},
    {"id": 2, "name": "UFC NFT", "image": "https://i.ibb.co/3N0fM1q/ufc.jpg", "original_price": 150},
    {"id": 3, "name": "Snoop Dogg NFT", "image": "https://i.ibb.co/0s9sH5r/snoop.jpg", "original_price": 200},
    {"id": 4, "name": "CryptoPunk", "image": "https://i.ibb.co/V3kM1hB/cryptopunk.jpg", "original_price": 120},
    {"id": 5, "name": "Bored Ape", "image": "https://i.ibb.co/WzcR7Jr/boredape.jpg", "original_price": 250},
    {"id": 6, "name": "Art Blocks", "image": "https://i.ibb.co/JpkFjVd/artblocks.jpg", "original_price": 180},
    {"id": 7, "name": "Cool Cat", "image": "https://i.ibb.co/tcZb1Z7/coolcat.jpg", "original_price": 90},
    {"id": 8, "name": "Meebits", "image": "https://i.ibb.co/FsDb7J2/meebits.jpg", "original_price": 130},
    {"id": 9, "name": "World of Women", "image": "https://i.ibb.co/hZZpVY8/wow.jpg", "original_price": 160},
    {"id": 10, "name": "Hashmasks", "image": "https://i.ibb.co/3Y6v5Xk/hashmasks.jpg", "original_price": 140},
    {"id": 11, "name": "BAYC NFT", "image": "https://i.ibb.co/3vQ7mY5/bayc.jpg", "original_price": 300},
    {"id": 12, "name": "Mutant Ape", "image": "https://i.ibb.co/4j6mrYV/mutant.jpg", "original_price": 220},
    {"id": 13, "name": "Pudgy Penguins", "image": "https://i.ibb.co/N9GHtCt/pudgy.jpg", "original_price": 110},
    {"id": 14, "name": "VeeFriends", "image": "https://i.ibb.co/9Vt4zCt/veefriends.jpg", "original_price": 170},
    {"id": 15, "name": "Cool Dogs NFT", "image": "https://i.ibb.co/2d0zXyG/cooldogs.jpg", "original_price": 95},
]

# Главная клавиатура магазина
def shop_menu():
    markup = InlineKeyboardMarkup()
    for nft in nfts:
        price = int(nft["original_price"] * 0.8)  # минус 20%
        btn = InlineKeyboardButton(
            text=f"{nft['name']} ⭐{price}",
            callback_data=f"nft_{nft['id']}"
        )
        markup.add(btn)
    return markup

# Клавиатура действий для конкретной NFT
def nft_actions(nft_id):
    nft = next((x for x in nfts if x["id"] == nft_id), None)
    if nft is None:
        return InlineKeyboardMarkup()
    price = int(nft["original_price"] * 0.8)
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            text=f"💬 Contact Seller (@ronaldureal) ⭐{price}",
            url="https://t.me/ronaldureal"
        ),
        InlineKeyboardButton(
            text="⬅ Back to Shop",
            callback_data="back_shop"
        )
    )
    return markup

# Старт бота
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "🎉 Добро пожаловать в наш NFT Shop!\n"
        "Здесь вы можете выбрать любую NFT и приобрести её на 20% дешевле оригинальной цены.",
        reply_markup=shop_menu()
    )

# Обработка нажатий кнопок
@dp.callback_query()
async def handle_callbacks(callback: types.CallbackQuery):
    data = callback.data
    if data.startswith("nft_"):
        nft_id = int(data.split("_")[1])
        nft = next((x for x in nfts if x["id"] == nft_id), None)
        if nft:
            await callback.message.answer_photo(
                photo=nft["image"],
                caption=f"{nft['name']}\nОригинальная цена: ⭐{nft['original_price']}\nСкидка: 20%",
                reply_markup=nft_actions(nft_id)
            )
    elif data == "back_shop":
        await callback.message.answer(
            "Вернулись в магазин NFT:",
            reply_markup=shop_menu()
        )
    await callback.answer()  # Чтобы убрать "часики" в Telegram

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
