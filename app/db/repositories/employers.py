from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text


class EmployerRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def is_email_taken(self, email: str) -> bool:
        query = text("SELECT 1 FROM employers WHERE email = :email")
        result = await self.db_session.execute(query, {"email": email})
        return result.scalar() is not None

    async def create_employer(self, employer_data: dict):
        query = text("""
            INSERT INTO employers (email, phone, password, company_name, address, about_company)
            VALUES (:email, :phone, :password, :company_name, :address, :about_company)
            RETURNING id;
        """)
        result = await self.db_session.execute(query, employer_data)
        await self.db_session.commit()
        return result.scalar()
