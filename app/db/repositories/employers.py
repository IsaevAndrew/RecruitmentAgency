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

    async def get_employer_by_id(self, employer_id: int):
        query = text("""
            SELECT id, company_name, email, phone, address, about_company
            FROM employers
            WHERE id = :id
        """)
        result = await self.db_session.execute(query, {"id": employer_id})
        return result.fetchone()

    async def update_employer(self, employer_id: int, updated_data: dict):
        query = text("""
            UPDATE employers
            SET company_name = :company_name,
                email = :email,
                phone = :phone,
                address = :address,
                about_company = :about_company
            WHERE id = :id
        """)
        await self.db_session.execute(query,
                                      {**updated_data, "id": employer_id})
        await self.db_session.commit()
