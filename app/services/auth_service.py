import bcrypt

from app.db.repositories.auth import AuthRepository
from fastapi import HTTPException


class AuthService:
    def __init__(self, repo: AuthRepository):
        self.repo = repo

    async def authenticate_candidate(self, email: str, password: str):
        user = await self.repo.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=401,
                                detail="Неверный email или пароль")

        if not bcrypt.checkpw(password.encode('utf-8'),
                              user.password.encode('utf-8')):
            raise HTTPException(status_code=401,
                                detail="Неверный email или пароль")

        return user

    async def authenticate_employer(self, email: str, password: str):
        employer = await self.repo.get_employer_by_email(email)
        if not employer:
            raise HTTPException(status_code=401,
                                detail="Неверный email или пароль")

        if not bcrypt.checkpw(password.encode('utf-8'),
                              employer.password.encode('utf-8')):
            raise HTTPException(status_code=401,
                                detail="Неверный email или пароль")

        return employer
