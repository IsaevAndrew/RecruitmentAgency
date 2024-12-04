from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.dependencies import get_db
from app.services.session_service import get_current_user
from app.services.application_service import ApplicationService

router = APIRouter()


# Pydantic модель для тела запроса
class ApplicationRequest(BaseModel):
    vacancy_id: int


@router.post("/applications")
async def apply_for_vacancy(
        request: Request,
        application_data: ApplicationRequest,  # Читаем vacancy_id из тела
        db: AsyncSession = Depends(get_db)
):
    current_user = get_current_user(request)
    if current_user["role"] != "candidate":
        raise HTTPException(status_code=403, detail="Доступ запрещен")

    service = ApplicationService(db_session=db)
    await service.create_application(
        candidate_id=current_user["user_id"],
        vacancy_id=application_data.vacancy_id
    )
    return {"message": "Отклик успешно отправлен"}
