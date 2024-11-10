from pathlib import Path
import uvicorn
from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from typing import Optional, Dict, Any
import os
import json
from core import core  # Импорт функции core из модуля core
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Указание директории для временных файлов и статических файлов
TEMP_DIR = "./temp_files"
os.makedirs(TEMP_DIR, exist_ok=True)

# Функция для преобразования set в list при сериализации JSON
def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

@app.post("/process_ifc")
async def upload_ifc(
    request: Request,
    ifc_file: UploadFile = File(...)  # обязательный файл
):

    # Получение всех параметров из запроса (кроме файла)
    form_data = await request.form()
    optional_params = {key: form_data[key] for key in form_data if key != "ifc_file"}

    # Печать параметров, которые пришли по REST API
    print(f"Received parameters:")
    print(f"File name: {ifc_file.filename}")
    for key, value in optional_params.items():
        print(f"{key}: {value}")

    # Сохранение файла в указанной директории
    temp_file_path = os.path.join(TEMP_DIR, ifc_file.filename)
    with open(temp_file_path, "wb") as temp_file:
        file_content = await ifc_file.read()
        temp_file.write(file_content)

    # Обработка параметров с использованием значений по умолчанию при отсутствии значений
    tolerance_value = optional_params.get("tolerance", "0.002")
    height_value = optional_params.get("height", "200e-3")
    width_value = optional_params.get("width", "100e-3")
    length_value = optional_params.get("length", "1.5")

    # Создание словаря данных для передачи в core с параметрами по умолчанию
    request_data = dict(
        fpath=Path(temp_file_path),
        pairs=[
            ("IfcWall", "IfcWall"),
            ("IfcWall", "IfcBeam"),
            ("IfcWall", "IfcColumn"),
            ("IfcBeam", "IfcBeam"),
            ("IfcBeam", "IfcColumn"),
            ("IfcColumn", "IfcColumn"),
        ],
        tolerance=float(tolerance_value) if tolerance_value else 0.002,
        merge_distance=0.1,
        filter_dimensions={
            "height": float(height_value) if height_value else 200e-3,
            "width": float(width_value) if width_value else 100e-3,
            "length": float(length_value) if length_value else 1.5
        },
        is_all=True
    )

    # Вызов функции core и получение результата
    result = core(**request_data)

    # Удаление временного файла после обработки
    os.remove(temp_file_path)

    # Возврат результата в виде JSON-ответа, преобразуя set в list
    return JSONResponse(content=json.loads(json.dumps(result, default=set_default)))

# Запуск сервера
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
