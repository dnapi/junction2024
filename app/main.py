from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    file_path = os.path.join("static", "index.html")
    with open(file_path, "r") as file:
        content = file.read()
    return HTMLResponse(content=content)

# Run the app using uvicorn
# uvicorn main:app --reload