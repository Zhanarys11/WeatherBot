# Default modules - Модули по умолчанию
import random
from os import system
from datetime import datetime

# Downloaded libraries - Скаченные библиотеки
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Created module - Созданный модуль
from static.image import IMAGE
from core.weather import weather_city
from static.stickers import S001

# Токен для работы с ботом
TOKEN = '6709343188:AAH__Mu00CL2Ptoa0y8tvpfU_RI4UIKJgHk'

# Айди администратора
ADMIN = '819533255'

system("clear")
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton("Зарегистрироваться", request_contact=True)
    )
    img_start = open(random.choice(IMAGE), 'rb')
    if message.from_user.username:
        await message.answer_photo(photo=img_start, 
        caption=f"Добро пожаловать {message.from_user.username} наш бот погоды включает прогноз погоды и мультимедийную систему аналитики, которая поможет вам прогнозировать погоду моментально пройдите регистрация для пользования.", reply_markup=markup)
    else:
        await message.answer_photo(photo=img_start, 
        caption=f"Добро пожаловать пользователь наш бот погоды включает прогноз погоды и мультимедийную систему аналитики, которая поможет вам прогнозировать погоду моментально пройдите регистрация для пользования.", reply_markup=markup)

    

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def contact_start(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton("Алматы"), KeyboardButton("Астана"), KeyboardButton("Атырау"),
        KeyboardButton("Тараз"), KeyboardButton("Шымкент"), KeyboardButton("Актобе"),
        KeyboardButton("Караганда"), KeyboardButton("Павлодар"), KeyboardButton("Уральск"),
        KeyboardButton("Семей"), KeyboardButton("Талдыкорган"), KeyboardButton("Усть-Каменогорск"),
    )

    user_id = message.contact.user_id
    username = message.chat.username
    first_name = message.contact.first_name
    last_name = message.contact.last_name
    phone = message.contact.phone_number

    Informations = f"""id: {user_id}
username: @{username}
first_name: {first_name}
last_name: {last_name}
phone: {phone}
created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

    registration_photo = open(random.choice(IMAGE), "rb")
    await bot.send_photo(ADMIN, registration_photo, Informations)
    await message.answer("Вы успешно зарегистрированы, теперь отправь название любого города!", reply_markup=markup)

    message_count = []
    @dp.message_handler(content_types=["text"])
    async def weather_city_author(message: types.Message):
        get_weather_def = weather_city(message.text)
        message_count.append(random.randint(0, 1))
        await message.reply(get_weather_def)

        if len(message_count) > random.randint(7, 10):
            await message.reply_sticker(random.choice(S001))
            message_count.clear()


if __name__ == "__main__":
    try:
        print(f"Бот запустился в {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        executor.start_polling(dp)
    except (KeyboardInterrupt, SystemExit):
        pass
