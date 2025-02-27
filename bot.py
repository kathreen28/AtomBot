import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Загружаем токен и ID сотрудника из переменных окружения
TOKEN = os.getenv("TOKEN")
EMPLOYEE_CHAT_ID = os.getenv("EMPLOYEE_CHAT_ID")

# Проверяем, загрузились ли переменные
if not TOKEN:
    raise ValueError("❌ Ошибка: Переменная окружения TOKEN не задана!")
if not EMPLOYEE_CHAT_ID:
    raise ValueError("❌ Ошибка: Переменная окружения EMPLOYEE_CHAT_ID не задана!")

# Преобразуем EMPLOYEE_CHAT_ID в int
EMPLOYEE_CHAT_ID = int(EMPLOYEE_CHAT_ID)

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)

# Создаем бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Основное меню
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Митап \"ИИ в действии: подключаем, тестируем, оптимизируем\"")],
        [KeyboardButton(text="Обратная связь"), KeyboardButton(text="Инструкции по нейросетям")]
    ],
    resize_keyboard=True
)

# Клавиатура для инструкций
instructions_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📘 Гид по ChatGPT")],
        [KeyboardButton(text="📘 Гид по Битрикс24 CoPilot")],
        [KeyboardButton(text="🔙 Назад")]
    ],
    resize_keyboard=True
)

# Обрабатываем команду /start
@dp.message(lambda message: message.text == "/start")
async def start_command(message: types.Message):
    welcome_text = (
        "Добро пожаловать! Я **Атом** — ваш цифровой помощник. 🤖\n\n"
        "Пока мои возможности ограничены, но со временем я стану еще полезнее.\n"
        "Если у вас есть предложения по улучшению — пишите!"
    )
    await message.answer(welcome_text, parse_mode="Markdown", reply_markup=main_keyboard)

# Обрабатываем нажатие кнопки "Инструкции по нейросетям"
@dp.message(lambda message: message.text == "Инструкции по нейросетям")
async def show_instructions(message: types.Message):
    await message.answer("Выберите инструкцию, которую хотите получить:", reply_markup=instructions_keyboard)

# Обрабатываем нажатие кнопки "📘 Гид по ChatGPT"
@dp.message(lambda message: message.text == "📘 Гид по ChatGPT")
async def send_chatgpt_guide(message: types.Message):
    file_path = "files/chatgpt_register_pay.pdf"  
    try:
        await message.answer_document(types.FSInputFile(file_path), caption="📘 Гид по ChatGPT\n\nРегистрация и подписка ChatGPT из России 🇷🇺")
    except Exception as e:
        await message.answer(f"Ошибка при отправке файла: {str(e)}")

# Обрабатываем нажатие кнопки "Гид по Битрикс24 CoPilot"
@dp.message(lambda message: message.text == "📘 Гид по Битрикс24 CoPilot")
async def send_bitrix_guide(message: types.Message):
    await message.answer("📘 **Гид по Битрикс24 CoPilot**\n\n"
                         "Полное руководство доступно по ссылке:\n"
                         "[Перейти к инструкции](https://helpdesk.bitrix24.ru/manual/copilot/)", 
                         parse_mode="Markdown")

# Обрабатываем кнопку "Назад" к основному меню
@dp.message(lambda message: message.text == "🔙 Назад")
async def go_back(message: types.Message):
    await message.answer("Вы вернулись в главное меню.", reply_markup=main_keyboard)

# Функция запуска бота
async def main():
    await dp.start_polling(bot)

# Запуск бота
if __name__ == "__main__":
    asyncio.run(main())
