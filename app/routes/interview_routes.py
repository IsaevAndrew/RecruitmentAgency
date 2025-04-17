from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates

from app.db.dependencies import get_db
from app.services.session_service import get_current_user
from app.services.interview_service import InterviewService

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get(
    "/",
    include_in_schema=False
)
async def get_candidate_interviews(
        request: Request,
        db: AsyncSession = Depends(get_db)
):
    current_user = get_current_user(request)
    service = InterviewService(db)

    if current_user["role"] == "candidate":
        interviews = await service.get_interviews_by_candidate(
            current_user["user_id"])
        return templates.TemplateResponse(
            "candidate_interviews.html",
            {"request": request, "interviews": interviews}
        )
    elif current_user["role"] == "employer":
        interviews = await service.get_pending_interviews_by_employer(
            current_user["user_id"])
        return templates.TemplateResponse(
            "employer_interviews.html",
            {"request": request, "interviews": interviews}
        )


@router.post(
    "/{interview_id}/accept",
    tags=["interviews"],
    summary="Принять собеседование",
    description="Обновляет результат собеседования как 'принято'"
)
async def accept_interview(
        interview_id: int,
        db: AsyncSession = Depends(get_db)
):
    service = InterviewService(db)
    await service.update_interview_result(interview_id=interview_id,
                                          result=True)
    return {"message": "Собеседование принято"}


@router.post(
    "/{interview_id}/reject",
    tags=["interviews"],
    summary="Отклонить собеседование",
    description="Обновляет результат собеседования как 'отклонено'"
)
async def reject_interview(
        interview_id: int,
        db: AsyncSession = Depends(get_db)
):
    service = InterviewService(db)
    await service.update_interview_result(interview_id=interview_id,
                                          result=False)
    return {"message": "Собеседование отклонено"}


@router.get(
    "/create_contract/{interview_id}",
    include_in_schema=False
)
async def create_contract(
        interview_id: int,
        request: Request,
        db: AsyncSession = Depends(get_db)
):
    service = InterviewService(db)
    interview = await service.get_interview_by_id(interview_id)

    if not interview:
        raise HTTPException(status_code=404, detail="Собеседование не найдено")

    await service.update_interview_result(interview_id=interview_id,
                                          result=True)

    return templates.TemplateResponse(
        "create_contract.html",
        {
            "request": request,
            "candidate_id": interview["candidate_id"],
            "vacancy_id": interview["vacancy_id"],
            "employer_id": interview["employer_id"]
        }
    )
