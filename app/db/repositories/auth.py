from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
import bcrypt


class AuthRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_user_by_email(self, email: str):
        query = text(
            "SELECT id, email, password FROM candidates WHERE email = :email")
        result = await self.db_session.execute(query, {"email": email})
        return result.fetchone()

    async def get_employer_by_email(self, email: str):
        query = text(
            "SELECT id, email, password FROM employers WHERE email = :email")
        result = await self.db_session.execute(query, {"email": email})
        return result.fetchone()
