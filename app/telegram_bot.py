import asyncio
from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import os
from memory_store import store
from ai.llm_processing import llm_processor
from dotenv import load_dotenv
import os
# Создаем бота и диспетчер
load_dotenv(".env")

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
BOT_TOKEN = str(BOT_TOKEN)

bot = Bot(token=BOT_TOKEN)
router = Router()  # Используем Router вместо Dispatcher

# Функция для отображения данных в виде таблицы
def create_feature_table(features):
    table = "Данные для проверки:\n"
    for i, (key, value) in enumerate(features.items(), 1):
        table += f"{i}. {key}: {value}\n"
    return table

@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Добро пожаловать! Отправьте текст для анализа.")

@router.message()
async def process_text(message: types.Message):
    text = message.text
    features = llm_processor.extract_features(text)
    store.add_user_data(message.from_user.id, features)
    
    table = create_feature_table(features)
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm")],
        [InlineKeyboardButton(text="✏️ Редактировать", callback_data="edit")]
    ])
    await message.answer(table, reply_markup=markup)

@router.callback_query(lambda c: c.data in ["confirm", "edit"])
async def handle_confirmation(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if callback_query.data == "confirm":
        data = store.get_user_data(user_id)
        await bot.send_message(callback_query.from_user.id, f"Данные отправлены: {data}")
        # Здесь можно отправить данные другой модели через FastAPI
        store.clear_user_data(user_id)
    elif callback_query.data == "edit":
        await bot.send_message(callback_query.from_user.id, "Отправьте изменения в формате key:value.")
    await callback_query.answer()

@router.message(lambda message: ":" in message.text)
async def edit_data(message: types.Message):
    key, value = map(str.strip, message.text.split(":", 1))
    user_id = message.from_user.id
    if store.update_user_data(user_id, key, value):
        await message.answer(f"Значение {key} обновлено на {value}.")
    else:
        await message.answer(f"Фича {key} не найдена.")

async def main():
    dp = Dispatcher()
    dp.include_router(router)

    # Запуск поллинга
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
