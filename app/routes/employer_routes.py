from fastapi import APIRouter, Form, HTTPException, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import HTMLResponse, RedirectResponse

from app.services.employer_service import EmployerService
from fastapi.templating import Jinja2Templates
from app.db.dependencies import get_db
from app.db.repositories.employers import EmployerRepository
from app.services.session_service import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post("/register/employer")
async def register_employer(
        request: Request,
        email: str = Form(...),
        phone: str = Form(...),
        password: str = Form(...),
        confirm_password: str = Form(...),
        company_name: str = Form(...),
        address: str = Form(...),
        about_company: str = Form(None),
        db: AsyncSession = Depends(get_db)
):
    service = EmployerService(repo=EmployerRepository(db_session=db))
    employer_data = {
        "email": email,
        "phone": phone,
        "password": password,
        "confirm_password": confirm_password,
        "company_name": company_name,
        "address": address,
        "about_company": about_company,
    }

    try:
        employer_id = await service.create_employer(employer_data)
        request.session["user_id"] = employer_id
        request.session["role"] = "employer"
        return RedirectResponse(url="/profile/employer", status_code=303)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/profile/employer", response_class=HTMLResponse)
async def get_employer_profile(
        request: Request,
        db: AsyncSession = Depends(get_db)
):
    current_user = get_current_user(request)
    if current_user["role"] != "employer":
        return {"error": "Доступ запрещен"}

    employer_service = EmployerService(repo=EmployerRepository(db_session=db))
    employer = await employer_service.get_employer_profile(
        current_user["user_id"])

    return templates.TemplateResponse(
        "employer_profile.html", {"request": request, "employer": employer}
    )


@router.post("/profile/employer/save")
async def save_employer_profile(
        request: Request,
        company_name: str = Form(...),
        email: str = Form(...),
        phone: str = Form(...),
        address: str = Form(None),
        about_company: str = Form(None),
        db: AsyncSession = Depends(get_db)
):
    current_user = get_current_user(request)
    if current_user["role"] != "employer":
        raise HTTPException(status_code=403, detail="Доступ запрещен")

    employer_service = EmployerService(repo=EmployerRepository(db_session=db))
    await employer_service.update_employer_profile(current_user["user_id"], {
        "company_name": company_name,
        "email": email,
        "phone": phone,
        "address": address,
        "about_company": about_company,
    })
    return {"status": "success", "message": "Данные успешно обновлены"}
    # employer = await employer_service.get_employer_profile(
    #     current_user["user_id"])

    # return templates.TemplateResponse(
    #     "employer_profile.html",
    #     {"request": request, "employer": employer}
    # )
