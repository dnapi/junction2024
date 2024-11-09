import uvicorn
from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import JSONResponse
import os

app = FastAPI()

# Указание директории для временных файлов
TEMP_DIR = "./temp_files"
os.makedirs(TEMP_DIR, exist_ok=True)

# Модель фильтра для элементов
class ElementFilter(BaseModel):
    length: Optional[float] = None
    height: Optional[float] = None
    width: Optional[float] = None
    tolerance: Optional[float] = None

# Скелет функции обработки данных
def process_ifc_data(request_data: dict):
    # Заглушка для будущей реализации
    print("Полученные данные для обработки:", request_data)
    return "OK"

# Основной маршрут для загрузки файла и фильтра
@app.post("/process_ifc")
async def upload_ifc(ifc_file: UploadFile = File(...),
                     length: Optional[float] = Form(None),
                     height: Optional[float] = Form(None),
                     width: Optional[float] = Form(None),
                     tolerance: Optional[float] = Form(None)):

    # Сохранение файла в указанной директории
    temp_file_path = os.path.join(TEMP_DIR, ifc_file.filename)
    with open(temp_file_path, "wb") as temp_file:
        file_content = await ifc_file.read()
        temp_file.write(file_content)

    # Создание словаря данных для обработки
    request_data = dict(
        fpath=temp_file_path,
        tolerance=tolerance if tolerance is not None else 0.002,  # значение по умолчанию
        filter_dimensions={
            "height": height if height is not None else 200e-3,
            "width": width if width is not None else 100e-3,
            "length": length if length is not None else 1.5
        },
        is_all=True
    )

    # Вызов функции обработки
    result = process_ifc_data(request_data)
    
    return JSONResponse(content={"message": result})

# Запуск сервера
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
