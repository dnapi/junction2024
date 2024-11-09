import json
from pathlib import Path
from typing import Any, Dict, Optional

import uvicorn
from core import core  # Импорт функции core из модуля core
from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Указание директории для временных файлов и статических файлов
TEMP_DIR = Path("./temp_files").resolve()
STATIC_DIR = Path("./static").resolve()

TEMP_DIR.mkdir(exist_ok=True, parents=True)
STATIC_DIR.mkdir(exist_ok=True, parents=True)

# Подключение статических файлов
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# Маршрут для отдачи главной страницы
@app.get("/", response_class=HTMLResponse)
async def read_root():
    file_path = STATIC_DIR / "index.html"
    if not file_path.exists():
        print("File not found:", str(file_path))  # Отладочный вывод
        return HTMLResponse(content="index.html not found", status_code=404)
    with open(file_path, "r") as file:
        content = file.read()
    return HTMLResponse(content=content)


# Функция для преобразования set в list при сериализации JSON
def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


@app.post("/api/upload")
async def upload_ifc(
    request: Request, ifc_file: UploadFile = File(...)  # обязательный файл
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
    ftmp = Path(TEMP_DIR) / ifc_file.filename
    with open(ftmp, "wb") as temp_file:
        file_content = await ifc_file.read()
        temp_file.write(file_content)

    # Вызов функции core и получение результата
    result = core(
        fpath=Path(ftmp),
        pairs=[
            ("IfcWall", "IfcWall"),
            ("IfcWall", "IfcBeam"),
            ("IfcWall", "IfcColumn"),
            ("IfcBeam", "IfcBeam"),
            ("IfcBeam", "IfcColumn"),
            ("IfcColumn", "IfcColumn"),
        ],
        tolerance=float(optional_params.get("tolerance", 0.002)),
        merge_distance=0.1,
        filter_dimensions={
            "height": float(optional_params.get("height", 200e-3)),
            "width": float(optional_params.get("width", 100e-3)),
            "length": float(optional_params.get("length", 1.5)),
        },
        is_all=True,
    )

    # Удаление временного файла после обработки
    ftmp.unlink()

    # Возврат результата в виде JSON-ответа, преобразуя set в list
    return JSONResponse(content=json.loads(json.dumps(result, default=set_default)))


# Запуск сервера
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
