from fastapi import APIRouter, Depends, Request, HTTPException, Form, Query
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.db.dependencies import get_db
from app.services.session_service import get_current_user
from app.services.vacancy_service import VacancyService
from app.db.repositories.vacancies import VacancyRepository

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get(
    "/vacancies",
    summary="Просмотр всех вакансий",
    tags=["vacancies"],
    description="Отображает все вакансии"
)
async def get_all_vacancies(request: Request):
    current_user = get_current_user(request)
    if current_user["role"] == "employer":
        return templates.TemplateResponse("employer_vacancies.html",
                                          {"request": request})
    return templates.TemplateResponse("candidate_vacancies.html",
                                      {"request": request})


@router.get(
    "/my-vacancies",
    tags=["vacancies"],
    response_class=HTMLResponse,
    summary="Просмотр своих вакансий",
    description="Позволяет работодателю просматривать свои вакансии"
)
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
        "my_vacancies.html", {"request": request, "vacancies": vacancies}
    )


@router.get(
    "/create/vacancy",
    response_class=HTMLResponse,
    include_in_schema=False
)
async def render_create_vacancy_page(
        request: Request,
        db: AsyncSession = Depends(get_db)
):
    current_user = get_current_user(request)
    if current_user["role"] != "employer":
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    return templates.TemplateResponse("create_vacancy.html",
                                      {"request": request})


@router.post(
    "/create/vacancy",
    tags=["vacancies"],
    summary="Создать вакансию",
    description="Позволяет работодателю создать новую вакансию"
)
async def create_vacancy(
        request: Request,
        description: str = Form(..., description="Описание вакансии"),
        requirements: str = Form(..., description="Требования к кандидату"),
        position_id: int = Form(..., description="ID должности"),
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


@router.post(
    "/vacancies/{vacancy_id}/deactivate",
    tags=["vacancies"],
    summary="Деактивировать вакансию",
    description="Отключает отображение вакансии для соискателей"
)
async def deactivate_vacancy(
        vacancy_id: int,
        db: AsyncSession = Depends(get_db)
):
    service = VacancyService(repo=VacancyRepository(db))
    success = await service.deactivate_vacancy(vacancy_id)
    if not success:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    return {"message": "Vacancy deactivated successfully"}


@router.post(
    "/vacancies/{vacancy_id}/activate",
    tags=["vacancies"],
    summary="Активировать вакансию",
    description="Активирует вакансию, делая её видимой для кандидатов"
)
async def activate_vacancy(
        vacancy_id: int,
        db: AsyncSession = Depends(get_db)
):
    service = VacancyService(repo=VacancyRepository(db))
    success = await service.activate_vacancy(vacancy_id)
    if not success:
        raise HTTPException(status_code=404, detail="Vacancy not found")

    updated_vacancy = await service.get_vacancy_by_id(vacancy_id)
    return {
        "message": "Vacancy activated successfully",
        "publication_date": updated_vacancy["publication_date"]
    }


@router.get(
    "/vacancies/api",
    tags=["vacancies"],
    summary="Получить вакансии",
    description="Возвращает вакансии с фильтрацией по должностям и требованиям"
)
async def get_vacancies(
        request: Request,
        db: AsyncSession = Depends(get_db),
        positions: str = Query(None,
                               description="Список ID должностей через запятую"),
        requirements: str = Query(None, description="Поиск по требованиям")
):
    current_user = get_current_user(request)
    service = VacancyService(repo=VacancyRepository(db))

    if current_user["role"] == "employer":
        vacancies = await service.get_active_vacancies(
            positions=[int(p) for p in
                       positions.split(",")] if positions else None,
            requirements=requirements
        )
        return {"vacancies": vacancies}

    if current_user["role"] == "candidate":
        positions_list = [int(p) for p in
                          positions.split(",")] if positions else None
        vacancies = await service.get_vacancies_with_application_status(
            candidate_id=current_user["user_id"],
            positions=positions_list,
            requirements=requirements
        )
        return {"vacancies": vacancies}

    raise HTTPException(status_code=403, detail="Доступ запрещен")
