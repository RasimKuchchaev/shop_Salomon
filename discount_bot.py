from auth_data import token
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
from main import colection_data
import json

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_button = ["Кросовки", "Видеокарты", "Гречка"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_button)

    await message.answer("Товары со скидкой", reply_markup=keyboard)


@dp.message_handler(Text(equals="Кросовки"))
async def get_discount_sneakers(messages: types.Message):
    await messages.answer("Please waiting ...")

    colection_data()

    with open("data.json") as file:
        data = json.load(file)

    for item in data:
        card = f"{hlink(item.get('title'), item.get('link'))}\n" \
            f"{hbold('Категория:  ')} {item.get('category')}\n" \
            f"{hbold('Прайс:  ')} {item.get('price_base')}\n" \
            f"{hbold('Прайс со скидкой:  ')} {item.get('discountPercent')}%: {item.get('price_sale')}"

        await messages.answer(card)


def main():
    executor.start_polling(dp)

if __name__ == '__main__':
    main()
