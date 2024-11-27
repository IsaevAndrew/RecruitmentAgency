from fastapi import APIRouter, Form, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.dependencies import get_db
from app.services.auth_service import AuthService
from app.db.repositories.auth import AuthRepository
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/candidate")
async def login_candidate(
        email: str = Form(...),
        password: str = Form(...),
        db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(repo=AuthRepository(db_session=db))
    user = await auth_service.authenticate_candidate(email, password)
    # Здесь можно установить сессию или вернуть токен
    return JSONResponse({"status": "success", "user_id": user.id})


@router.post("/employer")
async def login_employer(
        email: str = Form(...),
        password: str = Form(...),
        db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(repo=AuthRepository(db_session=db))
    employer = await auth_service.authenticate_employer(email, password)
    return JSONResponse({"status": "success", "employer_id": employer.id})
