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
from fastapi.responses import FileResponse
import asyncio
import pandas as pd
import uvicorn
import numpy as np

app = FastAPI()

@app.get("/")
async def root():
    return {"Status code": "200"}

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    """Обработка загрузки CSV и возвращение изменённого файла."""
    if not file or not file.filename.endswith(".csv"):
        return {"error": "Please upload a CSV file."}

    # Чтение содержимого файла
    try:
        content = await file.read()
        data = pd.read_csv(BytesIO(content))
    except Exception as e:
        return {"error": f"Error while reading CSV file: {e}"}

    # Обработка данных
    try:
        # data = data[(data['Ni_rec'] < 1) & (data['Ni_rec'] > 0)]
        data['Ni_rec'] = np.random.uniform(0, 1, size=len(data))
        data["Processed"] = "Example"
    except Exception as e:
        return {"error": f"Error while processing CSV file: {e}"}

    # Сохранение обработанного файла
    try:
        output_filename = "processed_file.csv"
        data.to_csv(output_filename, index=False)
    except Exception as e:
        return {"error": f"Error while saving processed CSV file: {e}"}

    # Возвращение файла как ответа
    try:
        return FileResponse(
            path=output_filename,
            filename="processed_file.csv",
            media_type="text/csv"
        )
    except Exception as e:
        return {"error": f"Error while returning processed CSV file: {e}"}



def main():
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()