from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.consts import SESSION_SECRET_KEY
from app.routes.auth_routes import router as auth_router
from app.routes.candidate_routes import router as candidate_router
from app.routes.employer_routes import router as employer_router
from app.routes.vacancy_routes import router as vacancy_router
from app.routes.position_routes import router as position_router
from app.routes.application_routes import router as application_router
from app.routes.interview_routes import router as interview_router
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(candidate_router, prefix="")
app.include_router(employer_router, prefix="")
app.include_router(vacancy_router, prefix="")
app.include_router(position_router, prefix="")
app.include_router(application_router, prefix="")
app.include_router(interview_router, prefix="")

app.mount("/static", StaticFiles(directory="static"), name="static")
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


@app.get("/auth/register/employer", response_class=HTMLResponse)
async def register_employer(request: Request):
    return templates.TemplateResponse("employer_register.html",
                                      {"request": request})


@app.get("/auth/register/candidate", response_class=HTMLResponse)
async def register_candidate(request: Request):
    return templates.TemplateResponse("candidate_register.html",
                                      {"request": request})


@app.post("/register/employer", response_class=HTMLResponse)
async def register_employer(
        request: Request,
        email: str = Form(...),
        phone: str = Form(...),
        password: str = Form(...),
        confirm_password: str = Form(...),
        company_name: str = Form(...),
        address: str = Form(...),
        about_company: str = Form(None),
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


@app.post("/auth/logout", response_class=JSONResponse)
async def logout(request: Request):
    request.session.clear()
    return JSONResponse({"message": "Вы вышли из аккаунта."})
