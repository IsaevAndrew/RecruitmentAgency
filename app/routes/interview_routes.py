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
    if current_user["role"] != "candidate":
        raise HTTPException(status_code=403, detail="Доступ запрещен")

    service = InterviewService(db)
    interviews = await service.get_interviews_by_candidate(
        candidate_id=current_user["user_id"]
    )
    return templates.TemplateResponse(
        "candidate_interviews.html",
        {"request": request, "interviews": interviews}
    )
    return
