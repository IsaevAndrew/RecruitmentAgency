from datetime import datetime
from fastapi import APIRouter, Form, Request, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.candidate_service import CandidateService
from app.db.repositories.candidates import CandidateRepository
from fastapi.responses import HTMLResponse, RedirectResponse
from app.db.dependencies import get_db
from app.services.session_service import get_current_user
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post("/register/candidate")
async def register_candidate(
        request: Request,
        last_name: str = Form(...),
        first_name: str = Form(...),
        middle_name: str = Form(None),
        date_of_birth: str = Form(...),
        gender: str = Form(...),
        email: str = Form(...),
        phone: str = Form(...),
        password: str = Form(...),
        confirm_password: str = Form(...),
        city: str = Form(...),
        education: str = Form(None),
        work_experience: str = Form(None),
        skills: str = Form(None),
        db: AsyncSession = Depends(get_db)
):
    service = CandidateService(repo=CandidateRepository(db_session=db))
    candidate_data = {
        "last_name": last_name,
        "first_name": first_name,
        "middle_name": middle_name,
        "date_of_birth": date_of_birth,
        "gender": gender,
        "email": email,
        "phone": phone,
        "password": password,
        "confirm_password": confirm_password,
        "city": city,
        "education": education,
        "work_experience": work_experience,
        "skills": skills,
    }

    try:
        candidate_id = await service.create_candidate(candidate_data)
        request.session["user_id"] = candidate_id
        request.session["role"] = "candidate"
        return RedirectResponse(url="/profile/candidate", status_code=303)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/profile/candidate", response_class=HTMLResponse)
async def get_candidate_profile(
        request: Request,
        db: AsyncSession = Depends(get_db)
):
    current_user = get_current_user(request)
    if current_user["role"] != "candidate":
        raise HTTPException(status_code=403, detail="Доступ запрещен")

    print(current_user)
    candidate_service = CandidateService(
        repo=CandidateRepository(db_session=db))
    candidate = await candidate_service.get_candidate_profile(
        current_user["user_id"])

    return templates.TemplateResponse(
        "candidate_profile.html", {"request": request, "candidate": candidate}
    )


@router.post("/profile/candidate/save")
async def save_candidate_profile(
        request: Request,
        date_of_birth: str = Form(...),
        city: str = Form(...),
        education: str = Form(None),
        work_experience: str = Form(None),
        skills: str = Form(None),
        db: AsyncSession = Depends(get_db)
):
    current_user = get_current_user(request)
    if current_user["role"] != "candidate":
        raise HTTPException(status_code=403, detail="Доступ запрещен")

    try:
        # Конвертируем строку даты в объект datetime.date
        date_of_birth_obj = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Некорректный формат даты")

    candidate_service = CandidateService(
        repo=CandidateRepository(db_session=db))

    updated_data = {
        "date_of_birth": date_of_birth_obj,
        "city": city,
        "education": education,
        "work_experience": work_experience,
        "skills": skills,
    }

    await candidate_service.update_candidate_profile(current_user["user_id"],
                                                     updated_data)

    return {"message": "Данные успешно сохранены"}
