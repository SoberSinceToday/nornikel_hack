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


from fastapi import FastAPI
import asyncio
from .telegram_bot import *

app = FastAPI()
dp = Dispatcher(bot)
dp.include_router(router)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(dp.start_polling())

@app.get("/")
def read_root():
    return {"message": "Сервер работает! Telegram-бот запущен."}
