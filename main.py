import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import F

# Твой токен
BOT_TOKEN = "8710709672:AAHov0L0RHWeXOVBY3wnpIxk25-aL08g_rE"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# NFT коллекция
nfts = [
    {"id":1,"name":"Ramadan NFT","image":"https://i.imgur.com/8Q4rX9G.png","original_price":150},
    {"id":2,"name":"UFC NFT","image":"https://i.imgur.com/7oLMv2n.png","original_price":180},
    {"id":3,"name":"Snubdok NFT","image":"https://i.imgur.com/Z9xP5sK.png","original_price":125},
    {"id":4,"name":"Cyber Cat","image":"https://i.imgur.com/1BZgplQ.png","original_price":100},
    {"id":5,"name":"Space Ape","image":"https://i.imgur.com/F5r3iS4.png","original_price":160},
    {"id":6,"name":"Pixel Panda","image":"https://i.imgur.com/3hKXwFQ.png","original_price":130},
    {"id":7,"name":"Golden Dog","image":"https://i.imgur.com/4H9uQp2.png","original_price":140},
    {"id":8,"name":"Neon Lion","image":"https://i.imgur.com/5Vt7jLd.png","original_price":170},
    {"id":9,"name":"Crypto Whale","image":"https://i.imgur.com/6YdKs8e.png","original_price":200},
    {"id":10,"name":"Galaxy Fox","image":"https://i.imgur.com/9N8aW3K.png","original_price":155},
    {"id":11,"name":"Moon Rabbit","image":"https://i.imgur.com/0PlQd7H.png","original_price":145},
    {"id":12,"name":"Solar Bear","image":"https://i.imgur.com/2Hd7iK9.png","original_price":160},
    {"id":13,"name":"Quantum Owl","image":"https://i.imgur.com/7kVwP8N.png","original_price":175},
    {"id":14,"name":"Pixel Shark","image":"https://i.imgur.com/8JpLd6Q.png","original_price":190},
    {"id":15,"name":"Crypto Tiger","image":"https://i.imgur.com/3Gt2BvE.png","original_price":210},
]

# Функция для расчета цены со скидкой 20%
def discounted_price(price):
    return int(price * 0.8)

# Главное меню магазина
def shop_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    for nft in nfts:
        price = discounted_price(nft["original_price"])
        btn = InlineKeyboardButton(
            text=f"{nft['name']} ⭐{price} (-20%)",
            callback_data=f"open_{nft['id']}"
        )
        markup.add(btn)
    return markup

# Меню конкретного NFT
def nft_actions(nft_id):
    nft = next((x for x in nfts if x["id"] == nft_id), None)
    if nft is None:
        return InlineKeyboardMarkup()
    price = discounted_price(nft["original_price"])
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(text=f"💬 Contact Seller (@ronaldureal) ⭐{price}", callback_data=f"contact_{nft_id}"),
        InlineKeyboardButton(text="⬅ Back to Shop", callback_data="back_shop")
    )
    return markup

# Старт команды
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "🎉 Добро пожаловать в FortunaNFT! Здесь ты можешь купить уникальные NFT со скидкой 20%.",
        reply_markup=shop_menu()
    )

# Обработка нажатий на кнопки
@dp.callback_query(F.data.startswith("open_"))
async def open_nft(call: types.CallbackQuery):
    nft_id = int(call.data.split("_")[1])
    nft = next((x for x in nfts if x["id"] == nft_id), None)
    if nft:
        text = f"🎨 {nft['name']}\n" \
               f"💰 Original Price: ⭐{nft['original_price']}\n" \
               f"🔥 Discounted Price: ⭐{discounted_price(nft['original_price'])}\n" \
               f"Свяжись с продавцом чтобы купить NFT."
        await call.message.answer_photo(
            photo=nft["image"],
            caption=text,
            reply_markup=nft_actions(nft_id)
        )
    await call.answer()

@dp.callback_query(F.data=="back_shop")
async def back_shop(call: types.CallbackQuery):
    await call.message.answer("Главное меню магазина:", reply_markup=shop_menu())
    await call.answer()

@dp.callback_query(F.data.startswith("contact_"))
async def contact(call: types.CallbackQuery):
    await call.message.answer("Свяжись с продавцом: @ronaldureal")
    await call.answer()

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
