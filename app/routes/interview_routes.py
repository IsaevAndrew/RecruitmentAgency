from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.dependencies import get_db
from app.services.session_service import get_current_user
from app.services.interview_service import InterviewService
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/interviews")
async def get_candidate_interviews(
        request: Request,
        db: AsyncSession = Depends(get_db)
):
    current_user = get_current_user(request)
    if current_user["role"] == "candidate":
        service = InterviewService(db)
        interviews = await service.get_interviews_by_candidate(
            candidate_id=current_user["user_id"]
        )
        return templates.TemplateResponse(
            "candidate_interviews.html",
            {"request": request, "interviews": interviews}
        )
    elif current_user["role"] == "employer":
        service = InterviewService(db)
        interviews = await service.get_pending_interviews_by_employer(
            employer_id=current_user["user_id"]
        )
        return templates.TemplateResponse(
            "employer_interviews.html",
            {"request": request, "interviews": interviews}
        )


@router.post("/interviews/{interview_id}/accept")
async def accept_interview(
        interview_id: int,
        db: AsyncSession = Depends(get_db)
):
    service = InterviewService(db)
    await service.update_interview_result(
        interview_id=interview_id,
        result=True
    )


@router.post("/interviews/{interview_id}/reject")
async def reject_interview(
        interview_id: int,
        db: AsyncSession = Depends(get_db)
):
    service = InterviewService(db)
    await service.update_interview_result(
        interview_id=interview_id,
        result=False
    )


@router.get("/interviews/create_contract/{interview_id}")
async def create_contract(interview_id: int,
                          request: Request,
                          db: AsyncSession = Depends(get_db)):
    service = InterviewService(db)
    interview = await service.get_interview_by_id(interview_id)
    await service.update_interview_result(
        interview_id=interview_id,
        result=True
    )
    if not interview:
        raise HTTPException(status_code=404, detail="Собеседование не найдено")

    return templates.TemplateResponse(
        "create_contract.html",
        {
            "request": request,
            "candidate_id": interview["candidate_id"],
            "vacancy_id": interview["vacancy_id"],
            "employer_id": interview["employer_id"]
        }
    )
