from fastapi import APIRouter, Depends, Request, HTTPException, Form, Query
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import HTMLResponse, RedirectResponse
from app.db.dependencies import get_db
from app.services.session_service import get_current_user
from app.services.vacancy_service import VacancyService
from app.db.repositories.vacancies import VacancyRepository
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/vacancies")
async def get_all_vacancies(request: Request,
                            db: AsyncSession = Depends(get_db)):
    service = VacancyService(repo=VacancyRepository(db))
    vacancies = await service.get_active_vacancies()
    current_user = get_current_user(request)
    if current_user["role"] == "employer":
        return templates.TemplateResponse(
            "employer_vacancies.html",
            {"request": request, "vacancies": vacancies}
        )
    return templates.TemplateResponse(
        "candidate_vacancies.html",
        {"request": request, "vacancies": vacancies}
    )


@router.get("/my-vacancies", response_class=HTMLResponse)
async def get_my_vacancies(
        request: Request,
        db: AsyncSession = Depends(get_db)
):
    current_user = get_current_user(request)
    if current_user["role"] != "employer":
        raise HTTPException(status_code=403, detail="Доступ запрещен")

    vacancy_repo = VacancyRepository(db_session=db)
    vacancies = await vacancy_repo.get_vacancies_by_employer(
        current_user["user_id"])

    return templates.TemplateResponse(
        "my_vacancies.html",
        {"request": request, "vacancies": vacancies}
    )


@router.get("/create/vacancy", response_class=HTMLResponse)
async def render_create_vacancy_page(
        request: Request,
        db: AsyncSession = Depends(get_db)
):
    current_user = get_current_user(request)
    if current_user["role"] != "employer":
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    return templates.TemplateResponse(
        "create_vacancy.html",
        {"request": request}
    )


@router.post("/create/vacancy")
async def create_vacancy(
        request: Request,
        description: str = Form(...),
        requirements: str = Form(...),
        position_id: int = Form(...),
        db: AsyncSession = Depends(get_db)
):
    current_user = get_current_user(request)
    if current_user["role"] != "employer":
        raise HTTPException(status_code=403, detail="Доступ запрещен")

    vacancy_service = VacancyService(repo=VacancyRepository(db))
    vacancy_data = {
        "description": description,
        "requirements": requirements,
        "is_active": True,
        "employer_id": current_user["user_id"],
        "position_id": position_id
    }
    await vacancy_service.create_vacancy(vacancy_data)
    return RedirectResponse(url="/my-vacancies", status_code=303)


@router.post("/vacancies/{vacancy_id}/deactivate")
async def deactivate_vacancy(vacancy_id: int,
                             db: AsyncSession = Depends(get_db)):
    service = VacancyService(repo=VacancyRepository(db))
    success = await service.deactivate_vacancy(vacancy_id)
    if not success:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    return {"message": "Vacancy deactivated successfully"}


@router.post("/vacancies/{vacancy_id}/activate")
async def activate_vacancy(vacancy_id: int, db: AsyncSession = Depends(get_db)):
    service = VacancyService(repo=VacancyRepository(db))
    success = await service.activate_vacancy(vacancy_id)
    if not success:
        raise HTTPException(status_code=404, detail="Vacancy not found")

    updated_vacancy = await service.get_vacancy_by_id(vacancy_id)
    return {
        "message": "Vacancy activated successfully",
        "publication_date": updated_vacancy["publication_date"]
    }


@router.get("/vacancies/api")
async def get_vacancies(
        request: Request,
        db: AsyncSession = Depends(get_db),
        positions: str = Query(None),
        requirements: str = Query(None)
):
    current_user = get_current_user(request)
    if current_user["role"] != "candidate":
        raise HTTPException(status_code=403, detail="Доступ запрещен")

    service = VacancyService(repo=VacancyRepository(db))
    positions_list = [int(p) for p in
                      positions.split(",")] if positions else None
    vacancies = await service.get_vacancies_with_application_status(
        candidate_id=current_user["user_id"],
        positions=positions_list,
        requirements=requirements
    )
    return {"vacancies": vacancies}
