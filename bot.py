import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from Uan import valuty, valuty2, Foto,Foto1, Foto10, Foto100
import requests
import json

TOKEN = '6899540654:AAGXvZu6Hy0TVzgWLHNtE7epmzZE_vrxoas'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
ADMINS = [5116352650]

@dp.message_handler(commands='start')
async def start(message: types.Message):
    valuty_choice = InlineKeyboardMarkup()
    for val in valuty:
        button = InlineKeyboardButton(text=val, callback_data=val)
        valuty_choice.add(button)
    await message.answer(text='Привіт! Я - бот-Змін валют.\n /start -показує валюти бота.\n /Uan -ви вибираєте скільки гривень ви хочете перевести',
                         reply_markup=valuty_choice)

@dp.callback_query_handler()
async def get_film_info(callback_query: types.CallbackQuery):
    if callback_query.data in valuty.keys():
        a = valuty[callback_query.data]["1 "]
        b = valuty[callback_query.data]["1 гривня"]
        message = f"1 {callback_query.data} = {a}, 1 гривня = {b}"
        await bot.send_message(callback_query.message.chat.id, message, parse_mode='html')
    else:
        await bot.send_message(callback_query.message.chat.id, 'Валюту не знайдено😟')

@dp.message_handler(commands='Uan')
async def Uan(message: types.Message,state: FSMContext):
    await message.answer(text='Скільки ви хочете перевисти гривень?')
    await state.set_state('set_Uan')

many=0

@dp.message_handler(state='set_Uan')
async def Uan2(message: types.Message,state: FSMContext):
    global many
    many = message.text
    valuty_choice = InlineKeyboardMarkup()
    for val in valuty2:
        button = InlineKeyboardButton(text=val, callback_data=val)
        valuty_choice.add(button)
    await message.answer(text='На яку валюту?', reply_markup=valuty_choice)
    await state.set_state('set_Uan2')

@dp.callback_query_handler(state='set_Uan2')
async def get_film_info(callback_query: types.CallbackQuery):
    if callback_query.data in valuty2.keys():
        a = valuty2[callback_query.data]
        message = f"{many} гривень перевили у {int(int(many) / a)} {callback_query.data}"
        await bot.send_message(callback_query.message.chat.id, message, parse_mode='html')

@dp.message_handler(commands='photoEvro')
async def photo(message: types.Message):
    with open(Foto, 'rb') as ph:
        photo = InputFile(ph)
        await bot.send_photo(message.chat.id, photo)

@dp.message_handler(commands='photoDolar')
async def photo_1(message: types.Message):
    with open(Foto1, 'rb') as ph:
        photo = InputFile(ph)
        await bot.send_photo(message.chat.id, photo)

@dp.message_handler(commands='photoBolgarLev')
async def photo_10(message: types.Message):
    with open(Foto10, 'rb') as ph:
        photo = InputFile(ph)
        await bot.send_photo(message.chat.id, photo)

@dp.message_handler(commands='photofuntsterling')
async def photo_100(message: types.Message):
    with open(Foto100, 'rb') as ph:
        photo = InputFile(ph)
        await bot.send_photo(message.chat.id, photo)


@dp.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://www.google.com/finance/quote/GBP-UAH?sa=X&ved=2ahUKEwi86MKg1uSCAxWtRPEDHYQAAk8QmY0JegQIEBAr&window=MAX')
    if res.status_code == 200:
        data = json.loads(res.text)
        bot.send_message(message, f'сейчас погода: {data["main"]["temp"]}')


    else:
        bot.send_message(message, f'город указан не верно')

    if __name__== '__main__':
        executor.start_polling(dp)