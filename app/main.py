from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Инициализация приложения FastAPI
app = FastAPI()

# Подключение папки со статическими файлами
app.mount("/static", StaticFiles(directory="static"), name="static")

# Настройка шаблонов
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_main(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/auth/candidate", response_class=HTMLResponse)
async def candidate_login(request: Request):
    return templates.TemplateResponse("candidate_login.html",
                                      {"request": request})


@app.get("/auth/employer", response_class=HTMLResponse)
async def employer_login(request: Request):
    return templates.TemplateResponse("employer_login.html",
                                      {"request": request})
