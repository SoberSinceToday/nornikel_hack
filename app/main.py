# from fastapi import FastAPI, Depends
# from sqlalchemy.ext.asyncio import AsyncSession
# from .database import init_db, SessionLocal
# from .db_models import Base
# from .schemas import UserCreate, UserOut
# from .crud import create_user, get_user_by_telegram_id
# import asyncio
# from .telegram_bot import dp

# app = FastAPI()

# async def get_db():
#     async with SessionLocal() as session:
#         yield session

# @app.on_event("startup")
# async def startup_event():
#     await init_db()
#     asyncio.create_task(dp.start_polling())

# @app.post("/users/", response_model=UserOut)
# async def create_new_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
#     return await create_user(db, user)

# @app.get("/users/{telegram_id}", response_model=UserOut)
# async def read_user(telegram_id: str, db: AsyncSession = Depends(get_db)):
#     user = await get_user_by_telegram_id(db, telegram_id)
#     if user is None:
#         return {"error": "User not found"}
#     return user


from io import BytesIO
import json  # For file storage
from fastapi import FastAPI, File, UploadFile
import asyncio
from .telegram_bot import *

app = FastAPI()

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    """Обработка загрузки CSV через FastAPI."""
    if not file.filename.endswith(".csv"):
        return {"error": "Please upload a CSV file."}

    content = await file.read()
    df = pd.read_csv(BytesIO(content))

    # Добавляем пример обработки (можно настроить)
    df["Processed"] = "Example"

    # Создаем и возвращаем обработанный файл
    output = BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)

    return {"filename": "processed_file.csv", "file_content": output.getvalue()}


async def main():
    dp = Dispatcher()
    dp.include_router(router)

    # Установка панели команд
    await set_bot_commands()

    # Запуск поллинга
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
