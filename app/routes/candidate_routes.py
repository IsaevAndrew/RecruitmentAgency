from fastapi import APIRouter, HTTPException, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.candidate_service import CandidateService
from app.db.repositories.candidates import CandidateRepository
from app.db.dependencies import get_db

router = APIRouter()


@router.post("/candidate")
async def register_candidate(
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
        return {"status": "success", "candidate_id": candidate_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
