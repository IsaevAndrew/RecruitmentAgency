from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text


class VacancyRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_active_vacancies(self):
        query = text("""
            SELECT v.id, v.description, v.requirements, v.publication_date, p.title AS position_title
            FROM vacancies v
            LEFT JOIN positions p ON v.position_id = p.id
            WHERE v.is_active = TRUE
        """)
        result = await self.db_session.execute(query)
        return [dict(row._mapping) for row in result]

    async def get_vacancies_by_employer(self, employer_id: int):
        query = text("""
            SELECT 
                v.id,
                v.description,
                v.requirements,
                v.publication_date,
                v.is_active,
                p.title AS position_title
            FROM vacancies v
            LEFT JOIN positions p ON v.position_id = p.id
            WHERE v.employer_id = :employer_id
            ORDER BY v.publication_date DESC
        """)
        result = await self.db_session.execute(query,
                                               {"employer_id": employer_id})
        return [dict(row._mapping) for row in result]

    async def create_vacancy(self, vacancy_data: dict):
        query = text("""
            INSERT INTO vacancies (description, requirements, publication_date, is_active, employer_id, position_id)
            VALUES (:description, :requirements, NOW(), :is_active, :employer_id, :position_id)
        """)
        await self.db_session.execute(query, vacancy_data)
        await self.db_session.commit()
