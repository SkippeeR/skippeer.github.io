from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.web_app_info import WebAppInfo
import json
import config

bot = Bot(config.BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('Открыть веб страницу', web_app=WebAppInfo(url = 'https://skippeer.github.io'))) #https://skippeer.github.io #https://webtelebot.devv/
    await message.answer('Привет!', reply_markup = markup)

@dp.message_handler(content_types=['web_app_data'])
async def web_app(message: types.Message):
    res = json.loads(message.web_app_data.data)
    # await message.answer(f'Товар: {res["name"]}\nЦена: {res["price"]}')
    num = str(res['price'])
    # num = num.replace(" ", "")
    print(num)
    num = num.split()
    num = ''.join(num)
    price = int(num) * 100
    #print(price)


    await bot.send_invoice(message.chat.id, 'Товары', ' ', 'invoice', config.PAYMENT_TOKEN, 'USD', [types.LabeledPrice(f'{res["name"]}', price)])

# @dp.message_handler(commands=['pay'])
# async def pay(message: types.Message):
#     await bot.send_invoice(message.chat.id, 'Название товара', 'Описание товара', 'invoice', config.PAYMENT_TOKEN, 'USD', [types.LabeledPrice('Название товара', 5 * 100)])

@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def succes(message: types.Message):
    await message.answer(f'Succes: {message.successful_payment.order_info}')

executor.start_polling(dp)