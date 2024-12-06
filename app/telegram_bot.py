import asyncio
import pandas as pd
from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    BotCommand,
    FSInputFile,
)
from aiogram.filters import Command
from aiogram import F
from dotenv import load_dotenv
import os

# # Загрузка токена из .env
# load_dotenv(".env")
# BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")

# # Проверяем, что токен загружен корректно
# if not BOT_TOKEN:
#     raise ValueError("BOT_TOKEN is not set in the .env file!")

# # Создаем бота и роутер
# bot = Bot(token=BOT_TOKEN)
# router = Router()

# # Функция для создания таблицы из словаря
# def create_feature_table(features):
#     table = "Данные для проверки:\n"
#     for i, (key, value) in enumerate(features.items(), 1):
#         table += f"{i}. {key}: {value}\n"
#     return table

# @router.message(Command("start"))
# async def start_handler(message: types.Message):
    # """Обработчик команды /start."""
    # await message.answer(
    #     "Добро пожаловать! 📊\n"
    #     "Вы можете:\n"
    #     "- Отправить текст для анализа.\n"
    #     "- Загрузить CSV-файл.\n"
    #     "- Получить результат в формате CSV.\n\n"
    #     "Введите /help для подробной информации.",
    #     reply_markup=ReplyKeyboardMarkup(
    #         keyboard=[
    #             [KeyboardButton(text="📤 Загрузить CSV")],
    #             [KeyboardButton(text="📋 Помощь (/help)")],
    #         ],
    #         resize_keyboard=True,
    #     ),
    # )

# @router.message(Command("help"))
# async def help_handler(message: types.Message):
#     """Обработчик команды /help."""
#     await message.answer(
#         "📋 Команды бота:\n"
#         "- /start: Запуск бота и отображение приветственного сообщения.\n"
#         "- /help: Информация о возможностях бота.\n"
#         "- 📤 Загрузить CSV: Отправьте CSV-файл, чтобы бот его обработал.\n\n"
#         "Вы можете:\n"
#         "1️⃣ Отправить текст, и бот выделит из него признаки (NER).\n"
#         "2️⃣ Отредактировать признаки через кнопки.\n"
#         "3️⃣ Загрузить CSV-файл для анализа и получить обработанный файл.",
#     )

# @router.message(F.document.mime_type == "text/csv")
# async def handle_csv_upload(message: types.Message):
#     """Обработчик загрузки CSV-файла."""
#     document_id = message.document.file_id
#     file_path = await bot.download(document_id)
    
#     # Чтение CSV-файла
#     try:
#         data = pd.read_csv(file_path)
#         # Пример обработки: добавление нового столбца
#         data["Processed"] = data.iloc[:, 0].apply(lambda x: len(str(x)))
#         processed_file_path = "processed_data.csv"
#         data.to_csv(processed_file_path, index=False)
        
#         # Отправка файла обратно пользователю
#         await message.answer_document(
#             FSInputFile(processed_file_path),
#             caption="Обработанный файл готов! 📂",
#         )
#     except Exception as e:
#         await message.answer(f"Произошла ошибка при обработке файла: {e}")

# @router.message()
# async def process_text(message: types.Message):
#     """Обработка текста и вывод признаков."""
#     text = message.text
#     # Пример признаков
#     features = {"Name": "Пример", "Length": len(text), "Text": text[:20]}
    
#     # Отображение в виде таблицы
#     table = create_feature_table(features)
#     markup = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm")],
#         [InlineKeyboardButton(text="✏️ Редактировать", callback_data="edit")],
#     ])
#     await message.answer(table, reply_markup=markup)

# @router.callback_query(lambda c: c.data in ["confirm", "edit"])
# async def handle_confirmation(callback_query: types.CallbackQuery):
#     """Обработка подтверждения или редактирования данных."""
#     user_id = callback_query.from_user.id
#     if callback_query.data == "confirm":
#         await bot.send_message(user_id, "Данные подтверждены и отправлены! ✅")
#     elif callback_query.data == "edit":
#         await bot.send_message(user_id, "Отправьте изменения в формате key:value.")
#     await callback_query.answer()

# async def set_bot_commands():
#     """Установка панели команд в Telegram."""
#     commands = [
#         BotCommand(command="/start", description="Начать работу с ботом"),
#         BotCommand(command="/help", description="Описание бота и его возможностей"),
#         BotCommand(command="/upload_csv", description="Загрузить CSV-файл"),
#     ]
#     await bot.set_my_commands(commands)

# async def main():
#     dp = Dispatcher()
#     dp.include_router(router)

#     # Установка панели команд
#     await set_bot_commands()

#     # Запуск поллинга
#     await dp.start_polling(bot)

# if __name__ == "__main__":
#     asyncio.run(main())


import asyncio
from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    BotCommand,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from aiogram.filters import Command
from dotenv import load_dotenv
import os
from datetime import datetime
import pandas as pd
from io import BytesIO

# Загрузка токена из .env
load_dotenv(".env")
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Проверяем, что токен загружен корректно
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in the .env file!")

# Создаем бота и роутер
bot = Bot(token=BOT_TOKEN)
router = Router()

# Словарь для хранения данных пользователя
user_data = {}


# Функция для создания более красивой таблицы
def create_beautiful_table(data):
    """
    Генерация текста таблицы и Inline-клавиатуры.
    """
    table = "📋 <b>Изменяемая таблица:</b>\n"
    table += "---------------------------------\n"
    for key, value in data.items():
        table += f"<b>{key}:</b> {value}\n"
    table += "---------------------------------\n"

    # Кнопка для редактирования значения
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"✏️ Изменить {key}", callback_data=f"edit_{key}")]
        for key in data
    ])
    return table, keyboard


@router.message(Command("start"))
async def start_handler(message: types.Message):
    """Обработчик команды /start."""
    await message.answer(
        "Добро пожаловать! 📊\n"
        "Вы можете:\n"
        "- Написать текст, а бот выделит нужные признаки и с помощью них сделает предикт.\n"
        "- Загрузить CSV-файл и получить обновлённый CSV-файл уже с таргетом.\n"
        "- Обновить или создать таблицу вручную.\n\n"
        "Введите /help для подробной информации.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="/help"), KeyboardButton(text="/table")],
                [KeyboardButton(text="/upload_csv")],
            ],
            resize_keyboard=True,
        ),
    )


@router.message(Command("help"))
async def help_handler(message: types.Message):
    """Обработчик команды /help."""
    await message.answer(
        "📋 Команды бота:\n"
        "- /start: Запуск бота и отображение приветственного сообщения.\n"
        "- /help: Информация о возможностях бота.\n"
        "- /table: Создание или редактирование таблицы.\n"
        "- /upload_csv: Загрузка CSV-файла для обработки.\n\n"
        "Вы можете:\n"
        "1️⃣ Редактировать признаки через таблицу.\n"
        "2️⃣ Загрузить CSV-файл для анализа и получить обработанный файл.",
    )


@router.message(Command("table"))
async def table_handler(message: types.Message):
    """Обработчик команды /table."""
    user_id = message.from_user.id

    # Инициализация данных пользователя
    if user_id not in user_data:
        user_data[user_id] = {"MEAS_DT": "2024-01-01 12:00:00"}  # Значение по умолчанию

    # Создаем таблицу
    table, keyboard = create_beautiful_table(user_data[user_id])

    # Отправляем таблицу пользователю
    await message.answer(
        "📝 Ваша изменяемая таблица. Вы можете редактировать значение `MEAS_DT`:\n\n" + table,
        reply_markup=keyboard,
        parse_mode="HTML",
    )
    


@router.callback_query(lambda c: c.data.startswith("edit_MEAS_DT"))
async def edit_column(callback_query: types.CallbackQuery):
    """Обработчик для редактирования MEAS_DT."""
    user_id = callback_query.from_user.id

    # Запрашиваем у пользователя новое значение
    await bot.send_message(
        user_id,
        "Введите новое значение для <b>MEAS_DT</b> (формат: YYYY-MM-DD HH:MM:SS):",
        parse_mode="HTML",
    )
    await callback_query.answer()


@router.message(lambda message: True)  # Обработчик любого текста
async def handle_new_value(message: types.Message):
    """Обработчик нового значения для MEAS_DT."""
    user_id = message.from_user.id

    # Проверяем, что пользователь инициализировал таблицу
    if user_id not in user_data:
        await message.answer("Пожалуйста, начните с команды /table.")
        return

    # Проверяем корректность формата даты
    try:
        datetime.strptime(message.text, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        await message.answer(
            "❌ Неверный формат даты!\n"
            "Пожалуйста, используйте формат: YYYY-MM-DD HH:MM:SS."
        )
        return

    # Сохраняем новое значение
    user_data[user_id]["MEAS_DT"] = message.text

    # Обновляем таблицу
    table, keyboard = create_beautiful_table(user_data[user_id])
    await message.answer(
        "✅ Таблица успешно обновлена:\n\n" + table,
        reply_markup=keyboard,
        parse_mode="HTML",
    )
    print(user_data)

# Модули подгрузки .csv

@router.message(Command("upload_csv"))
async def upload_csv_handler(message: types.Message):
    """Обработчик загрузки CSV."""
    await message.answer(
        "📂 Загрузите CSV-файл через вложение, чтобы бот его обработал."
    )


@router.message(lambda message: message.document)
async def process_csv_file(message: types.Message):
    """Обработка загруженного CSV-файла."""
    document = message.document

    # Проверка на CSV
    if not document.file_name.endswith(".csv"):
        await message.answer("❌ Пожалуйста, загрузите файл в формате CSV.")
        return

    # Загружаем файл
    file = await bot.download(document)
    df = pd.read_csv(file)

    # Добавляем пример обработки (можно настроить)
    df["Processed"] = "Example"

    # Возвращаем обработанный файл
    output = BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)

    await bot.send_document(
        message.chat.id,
        document=types.InputFile(output, filename="processed_file.csv"),
        caption="✅ Обработанный CSV-файл готов.",
    )


async def set_bot_commands():
    """Установка панели команд в Telegram."""
    commands = [
        BotCommand(command="/start", description="Начать работу с ботом"),
        BotCommand(command="/help", description="Описание бота и его возможностей"),
        BotCommand(command="/table", description="Создать или изменить таблицу вручную"),
        BotCommand(command="/upload_csv", description="Загрузить CSV-файл"),
    ]
    await bot.set_my_commands(commands)


async def main():
    dp = Dispatcher()
    dp.include_router(router)

    # Установка панели команд
    await set_bot_commands()

    # Запуск поллинга
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

