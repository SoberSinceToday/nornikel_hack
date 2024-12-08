from io import BytesIO
import json  # For file storage
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import asyncio
import pandas as pd
import uvicorn
import numpy as np

from PreparerPoolpsCsv import PreparerPoolpsCsv
from Solutioner import Solutioner
from utils import ni_rec_predict

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
        data.to_csv('data.csv')
        preparer = PreparerPoolpsCsv()
        preparer.load_dataset('data/df_hack_final.csv') # Передача содержимого как строки
        preparer.prepare_pulpas_dataset()
        df = preparer.get_pulpas_df()

    except Exception as e:
        return {"error": f"Error while reading CSV file: {e}"}

    # Обработка данных
    try:
        s = Solutioner(path_to_test_data='data.csv',
            path_to_train='data/df_hack_final.csv',
            pulpas_df=df)
        ans = s.get_ans()
        ans.to_csv('ans.csv')
    except Exception as e:
        return {"error": f"Error while processing CSV file: {e}"}

    # Сохранение обработанного файла
    try:
        output_filename = "processed_file.csv"
        ans.to_csv(output_filename, index=False)
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

