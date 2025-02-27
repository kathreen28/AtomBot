import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

# Вставьте сюда свой токен от BotFather
TOKEN = "7828644607:AAGLnk_AQJBJKnUlgDxr9oay4Yv5jXrhR-A"

# Telegram ID сотрудника, который будет получать обратную связь
EMPLOYEE_CHAT_ID = 323429558  

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)

# Создаем бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Основное меню
main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
button_meetup = KeyboardButton("Митап \"ИИ в действии: подключаем, тестируем, оптимизируем\"")
button_feedback = KeyboardButton("Обратная связь")
button_instructions = KeyboardButton("Инструкции по нейросетям")
main_keyboard.add(button_meetup, button_feedback, button_instructions)

# Клавиатура для инструкций
instructions_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
button_chatgpt_guide = KeyboardButton("📘 Гид по ChatGPT")
button_bitrix_guide = KeyboardButton("📘 Гид по Битрикс24 CoPilot")
button_back = KeyboardButton("🔙 Назад")
instructions_keyboard.add(button_chatgpt_guide, button_bitrix_guide, button_back)

# Обрабатываем команду /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    welcome_text = (
        "Добро пожаловать! Я **Атом** — ваш цифровой помощник. 🤖\n\n"
        "Пока мои возможности ограничены, но со временем я стану еще полезнее.\n"
        "Если у вас есть предложения по улучшению — пишите!"
    )
    await message.answer(welcome_text, parse_mode="Markdown", reply_markup=main_keyboard)

# Обрабатываем нажатие кнопки "Инструкции по нейросетям"
@dp.message_handler(lambda message: message.text == "Инструкции по нейросетям")
async def show_instructions(message: types.Message):
    await message.answer("Выберите инструкцию, которую хотите получить:", reply_markup=instructions_keyboard)

# Обрабатываем нажатие кнопки "📘 Гид по ChatGPT"
@dp.message_handler(lambda message: message.text == "📘 Гид по ChatGPT")
async def send_chatgpt_guide(message: types.Message):
    file_path = "files/chatgpt_register_pay.pdf"  # Укажи правильный путь к файлу
    try:
        await message.answer_document(types.InputFile(file_path), caption="📘 Гид по ChatGPT\n\nРегистрация и подписка ChatGPT из России 🇷🇺")
    except Exception as e:
        await message.answer(f"Ошибка при отправке файла: {str(e)}")

# Обрабатываем нажатие кнопки "Гид по Битрикс24 CoPilot"
@dp.message_handler(lambda message: message.text == "📘 Гид по Битрикс24 CoPilot")
async def send_bitrix_guide(message: types.Message):
    await message.answer("📘 **Гид по Битрикс24 CoPilot**\n\n"
                         "Полное руководство доступно по ссылке:\n"
                         "[Перейти к инструкции](https://helpdesk.bitrix24.ru/manual/copilot/)", 
                         parse_mode="Markdown")

# Обрабатываем кнопку "Назад" к основному меню
@dp.message_handler(lambda message: message.text == "🔙 Назад")
async def go_back(message: types.Message):
    await message.answer("Вы вернулись в главное меню.", reply_markup=main_keyboard)

# Запускаем бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
