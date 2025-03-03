import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import F

# Загружаем токен и ID сотрудника из переменных окружения
TOKEN = os.getenv("TOKEN")
EMPLOYEE_CHAT_ID = os.getenv("EMPLOYEE_CHAT_ID")

# Проверяем, загрузились ли переменные
if not TOKEN or TOKEN.strip() == "":
    raise ValueError("❌ Ошибка: Переменная окружения TOKEN не задана или пустая!")

if not EMPLOYEE_CHAT_ID or EMPLOYEE_CHAT_ID.strip() == "":
    raise ValueError("❌ Ошибка: Переменная окружения EMPLOYEE_CHAT_ID не задана или пустая!")

# Очищаем переменные от пробелов
TOKEN = TOKEN.strip()
EMPLOYEE_CHAT_ID = int(EMPLOYEE_CHAT_ID.strip())

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)

# Создаем бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Словарь для отслеживания состояния пользователей (ждём ли отзыв)
user_feedback_state = {}

# Основное меню
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Нейросети и «Атом»: синергия будущего")],
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
@dp.message(Command("start"))
async def start_command(message: types.Message):
    welcome_text = (
        "Добро пожаловать! Я **Атом** — ваш цифровой помощник. 🤖\n\n"
        "Пока мои возможности ограничены, но со временем я стану еще полезнее.\n"
        "Если у вас есть предложения по улучшению — пишите!"
    )
    await message.answer(welcome_text, parse_mode="Markdown", reply_markup=main_keyboard)

# Обрабатываем кнопку "Нейросети.."
@dp.message(F.text == "Нейросети и «Атом»: синергия будущего")
async def meetup_info(message: types.Message):
    response_text = (
        "📢 **\"Нейросети и «Атом»: синергия будущего\"**\n\n"
        "На встрече обсудим эффективность применения ИИ в работе, познакомимся с самыми популярными языковыми моделями попробуем их применение на практике. 🚀\n\n"
        "🔹 Дата и время: 04.03.2025 10:30\n"
        "🔹 Формат: онлайн/офлайн\n"
    )
    await message.answer(response_text, parse_mode="Markdown")

# Обрабатываем кнопку "Обратная связь"
@dp.message(F.text == "Обратная связь")
async def feedback_request(message: types.Message):
    user_feedback_state[message.from_user.id] = True  # Запоминаем, что ждём отзыв
    await message.answer("✍️ Напишите свой отзыв или предложение, и мы обязательно его рассмотрим!")

# Обрабатываем отправленный отзыв
@dp.message(lambda message: message.from_user.id in user_feedback_state)
async def receive_feedback(message: types.Message):
    user_id = message.from_user.id
    user_feedback_state.pop(user_id, None)  # Удаляем пользователя из состояния

    # Отправляем отзыв сотруднику
    feedback_text = f"📩 **Новый отзыв от @{message.from_user.username or message.from_user.full_name}:**\n\n{message.text}"
    await bot.send_message(EMPLOYEE_CHAT_ID, feedback_text)

    # Отвечаем пользователю
    await message.answer("✅ Спасибо за ваш отзыв! Мы обязательно его рассмотрим. 🤝", reply_markup=main_keyboard)

# Обрабатываем нажатие кнопки "Инструкции по нейросетям"
@dp.message(F.text == "Инструкции по нейросетям")
async def show_instructions(message: types.Message):
    await message.answer("Выберите инструкцию, которую хотите получить:", reply_markup=instructions_keyboard)

# Обрабатываем нажатие кнопки "📘 Гид по ChatGPT"
@dp.message(F.text == "📘 Гид по ChatGPT")
async def send_chatgpt_guide(message: types.Message):
    file_path = "files/chatgpt_register_pay.pdf"  
    try:
        await message.answer_document(types.FSInputFile(file_path), caption="📘 Гид по ChatGPT\n\nРегистрация и подписка ChatGPT из России 🇷🇺")
    except Exception as e:
        await message.answer(f"Ошибка при отправке файла: {str(e)}")

# Обрабатываем нажатие кнопки "📘 Гид по Битрикс24 CoPilot"
@dp.message(F.text == "📘 Гид по Битрикс24 CoPilot")
async def send_bitrix_guide(message: types.Message):
    await message.answer("📘 **Гид по Битрикс24 CoPilot**\n\n"
                         "Полное руководство доступно по ссылке:\n"
                         "[Перейти к инструкции](https://helpdesk.bitrix24.ru/manual/copilot/)", 
                         parse_mode="Markdown")

# Обрабатываем кнопку "🔙 Назад" к основному меню
@dp.message(F.text == "🔙 Назад")
async def go_back(message: types.Message):
    await message.answer("Вы вернулись в главное меню.", reply_markup=main_keyboard)

# Функция запуска бота
async def main():
    await dp.start_polling(bot)  # Запускаем бота

# Запуск бота
if __name__ == "__main__":
    asyncio.run(main())  # Запускаем асинхронный процесс
