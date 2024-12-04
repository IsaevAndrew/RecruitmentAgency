from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from datetime import datetime


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
            ORDER BY v.is_active DESC, v.publication_date DESC
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

    async def update_vacancy_status(self, vacancy_id: int,
                                    is_active: bool) -> bool:
        query = text("""
            UPDATE vacancies
            SET 
                is_active = :is_active,
                publication_date = CASE WHEN :is_active THEN :current_date ELSE publication_date END
            WHERE id = :vacancy_id
        """)
        current_date = datetime.utcnow()  # Текущая дата и время в формате UTC
        result = await self.db_session.execute(query, {
            "is_active": is_active,
            "current_date": current_date,
            "vacancy_id": vacancy_id
        })
        await self.db_session.commit()
        return result.rowcount > 0

    async def filter_vacancies(self, positions, requirements):
        query = """
            SELECT v.id, v.description, v.requirements, v.publication_date, p.title AS position_title
            FROM vacancies v
            JOIN positions p ON v.position_id = p.id
            WHERE v.is_active = TRUE
        """

        filters = []
        params = {}

        if positions:
            query += " AND v.position_id = ANY(:positions)"
            params["positions"] = positions

        if requirements:
            query += " AND LOWER(v.requirements) LIKE LOWER(:requirements)"
            params["requirements"] = f"%{requirements}%"

        result = await self.db_session.execute(text(query), params)

        # Используем .mappings() для возврата словарей
        return [row for row in result.mappings()]

    async def get_vacancy_by_id(self, vacancy_id: int):
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
            WHERE v.id = :vacancy_id
        """)
        result = await self.db_session.execute(query,
                                               {"vacancy_id": vacancy_id})
        row = result.fetchone()
        if row:
            return dict(row._mapping)
        return None
