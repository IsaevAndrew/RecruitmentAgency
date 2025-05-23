from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.dependencies import get_db
from app.db.repositories.applications import ApplicationRepository
from app.services.session_service import get_current_user
from app.services.application_service import ApplicationService
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


class ApplicationRequest(BaseModel):
    vacancy_id: int = Field(...,
                            description="Идентификатор вакансии, на которую подается отклик")


@router.post(
    "/applications",
    tags=["applications"],
    summary="Отклик на вакансию",
    description="Позволяет кандидату откликнуться на выбранную вакансию"
)
async def apply_for_vacancy(
        request: Request,
        application_data: ApplicationRequest,
        db: AsyncSession = Depends(get_db)
):
    current_user = get_current_user(request)
    if current_user["role"] != "candidate":
        raise HTTPException(status_code=403, detail="Доступ запрещен")

    service = ApplicationService(repo=ApplicationRepository(db))
    await service.create_application(
        candidate_id=current_user["user_id"],
        vacancy_id=application_data.vacancy_id
    )
    return {"message": "Отклик успешно отправлен"}


@router.get(
    "/my-applications",
    tags=["applications"],
    summary="Просмотр откликов на вакансии",
    description="Позволяет кандидату просмотреть отклики на вакансии"
)
async def get_my_applications(
        request: Request,
        db: AsyncSession = Depends(get_db)
):
    current_user = get_current_user(request)
    if current_user["role"] != "candidate":
        raise HTTPException(status_code=403, detail="Доступ запрещен")

    service = ApplicationService(repo=ApplicationRepository(db))
    applications = await service.get_applications_by_candidate(
        current_user["user_id"])

    return templates.TemplateResponse(
        "my_applications.html",
        {"request": request, "applications": applications}
    )
