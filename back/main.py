import json
import os
from pathlib import Path
from typing import Optional

import uvicorn
from core import core  # Импорт функции core из модуля core
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel

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


# Функция для преобразования set в list при сериализации JSON
def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


@app.post("/api/upload")
async def upload_ifc(
    ifc_file: UploadFile = File(...),
    length: Optional[float] = Form(None),
    height: Optional[float] = Form(None),
    width: Optional[float] = Form(None),
    tolerance: Optional[float] = Form(None),
):

    # Сохранение файла в указанной директории
    temp_file_path = os.path.join(TEMP_DIR, ifc_file.filename)
    with open(temp_file_path, "wb") as temp_file:
        file_content = await ifc_file.read()
        temp_file.write(file_content)

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
        tolerance=(
            tolerance if tolerance is not None else 0.002
        ),  # значение по умолчанию
        merge_distance=0.1,  # значение по умолчанию
        filter_dimensions={
            "height": height if height is not None else 200e-3,
            "width": width if width is not None else 100e-3,
            "length": length if length is not None else 1.5,
        },
        is_all=True,
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
