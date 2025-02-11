import asyncio
import logging
import random
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

# Вставь свой токен от BotFather
TOKEN = "7828644607:AAGLnk_AQJBJKnUlgDxr9oay4Yv5jXrhR-A"

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Создаём объекты бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Создаём кнопки
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Привет!"), KeyboardButton(text="Как дела?")],
        [KeyboardButton(text="Случайный факт"), KeyboardButton(text="Помощь")],
        [KeyboardButton(text="Посмотреть на котика")]
    ],
    resize_keyboard=True  # Уменьшаем кнопки под размер экрана
)

# Функция для получения случайного котика через API
async def get_random_cat():
    url = "https://api.thecatapi.com/v1/images/search"
    response = requests.get(url)
    if response.status_code == 200:
        cat_data = response.json()
        return cat_data[0]["url"]  # Берём ссылку на котика
    return None

# Обрабатываем команды
@dp.message()
async def handle_message(message: Message):
    if message.text == "/start":
        await message.answer("Привет! Выбери действие:", reply_markup=keyboard)

    elif message.text == "Привет!":
        await message.answer("Привет! Рад тебя видеть 😊")

    elif message.text == "Как дела?":
        await message.answer("У меня всё отлично! А у тебя?")

    elif message.text == "Случайный факт":
        await message.answer("Знаешь ли ты, что у улитки 14 000 зубов? 🐌")

    elif message.text == "Помощь":
        await message.answer("Я умею отвечать на сообщения, показывать кнопки и отправлять котиков!")

    elif message.text == "Посмотреть на котика":
        cat_image_url = await get_random_cat()  # Получаем случайную картинку котика
        if cat_image_url:
            await bot.send_photo(message.chat.id, cat_image_url, caption="Вот тебе котик! 🐱")
        else:
            await message.answer("Не удалось найти котика 😿 Попробуй ещё раз!")

# Функция запуска бота
async def main():
    dp["bot"] = bot  # Передаём бота в диспетчер
    await dp.start_polling(bot)

# Запускаем бота
if __name__ == "__main__":
    asyncio.run(main())
