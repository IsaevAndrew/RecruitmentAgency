from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from app.consts import SESSION_SECRET_KEY
from app.routes.auth_routes import router as auth_router
from app.routes.candidate_routes import router as candidate_router
from app.routes.employer_routes import router as employer_router
from app.routes.vacancy_routes import router as vacancy_router
from app.routes.position_routes import router as position_router
from app.routes.application_routes import router as application_router
from app.routes.interview_routes import router as interview_router
from app.routes.contracts_routes import router as contracts_router

app = FastAPI(
    title="Recruitment Agency API",
    description="API для взаимодействия с агентством по найму",
    version="2.0.0"
)

app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(candidate_router, prefix="")
app.include_router(employer_router, prefix="")
app.include_router(vacancy_router, prefix="")
app.include_router(position_router, prefix="/positions")
app.include_router(application_router, prefix="")
app.include_router(interview_router, prefix="/interviews")
app.include_router(contracts_router, prefix="/contracts")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def read_main(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/auth/candidate", response_class=HTMLResponse,
         include_in_schema=False)
async def candidate_login(request: Request):
    return templates.TemplateResponse("candidate_login.html",
                                      {"request": request})


@app.get("/auth/employer", response_class=HTMLResponse, include_in_schema=False)
async def employer_login(request: Request):
    return templates.TemplateResponse("employer_login.html",
                                      {"request": request})


@app.get("/auth/register/employer", response_class=HTMLResponse,
         include_in_schema=False)
async def register_employer(request: Request):
    return templates.TemplateResponse("employer_register.html",
                                      {"request": request})


@app.get("/auth/register/candidate", response_class=HTMLResponse,
         include_in_schema=False)
async def register_candidate(request: Request):
    return templates.TemplateResponse("candidate_register.html",
                                      {"request": request})


@app.post(
    "/register/employer",
    response_class=HTMLResponse,
    summary="Регистрация работодателя",
    description="Регистрирует нового работодателя на основе переданных данных формы"
)
async def register_employer(
        request: Request,
        email: str = Form(..., description="Электронная почта работодателя"),
        phone: str = Form(..., description="Номер телефона"),
        password: str = Form(..., description="Пароль"),
        confirm_password: str = Form(..., description="Подтверждение пароля"),
        company_name: str = Form(..., description="Название компании"),
        address: str = Form(..., description="Адрес компании"),
        about_company: str = Form(None, description="Описание компании"),
):
    print({
        "email": email,
        "phone": phone,
        "password": password,
        "confirm_password": confirm_password,
        "company_name": company_name,
        "address": address,
        "about_company": about_company,
    })
    return templates.TemplateResponse("home.html", {"request": request})


@app.post(
    "/auth/logout",
    response_class=JSONResponse,
    summary="Выход из аккаунта",
    description="Очищает сессию пользователя и выполняет выход из аккаунта"
)
async def logout(request: Request):
    request.session.clear()
    return JSONResponse({"message": "Вы вышли из аккаунта."})
