from fastapi import APIRouter, Form, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.dependencies import get_db
from app.services.auth_service import AuthService
from app.db.repositories.auth import AuthRepository
from fastapi.responses import RedirectResponse

router = APIRouter()


@router.post(
    "/candidate",
    tags=["auth"],
    summary="Вход для кандидата",
    description="Аутентифицирует кандидата по email и паролю и перенаправляет на страницу профиля"
)
async def login_candidate(
        request: Request,
        email: str = Form(..., description="Электронная почта кандидата"),
        password: str = Form(..., description="Пароль кандидата"),
        db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(repo=AuthRepository(db_session=db))
    user = await auth_service.authenticate_candidate(email, password)
    request.session["user_id"] = user.id
    request.session["role"] = "candidate"
    return RedirectResponse(url="/profile/candidate", status_code=303)


@router.post(
    "/employer",
    tags=["auth"],
    summary="Вход для работодателя",
    description="Аутентифицирует работодателя по email и паролю и перенаправляет на страницу профиля"
)
async def login_employer(
        request: Request,
        email: str = Form(..., description="Электронная почта работодателя"),
        password: str = Form(..., description="Пароль работодателя"),
        db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(repo=AuthRepository(db_session=db))
    employer = await auth_service.authenticate_employer(email, password)
    request.session["user_id"] = employer.id
    request.session["role"] = "employer"
    return RedirectResponse(url="/profile/employer", status_code=303)
