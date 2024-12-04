from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text


class ApplicationRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_application(self, candidate_id: int, vacancy_id: int):
        query = text("""
            INSERT INTO job_applications (candidate_id, vacancy_id, application_date)
            VALUES (:candidate_id, :vacancy_id, NOW())
        """)
        await self.db_session.execute(query, {"candidate_id": candidate_id,
                                              "vacancy_id": vacancy_id})
        await self.db_session.commit()

    async def get_applications_by_candidate(self, candidate_id: int):
        query = """
            SELECT 
                ja.application_date,
                v.id AS vacancy_id,
                v.description,
                v.requirements,
                v.publication_date,
                p.title AS position_title
            FROM job_applications ja
            JOIN vacancies v ON ja.vacancy_id = v.id
            LEFT JOIN positions p ON v.position_id = p.id
            WHERE ja.candidate_id = :candidate_id
            ORDER BY ja.application_date DESC
        """
        result = await self.db_session.execute(text(query),
                                               {"candidate_id": candidate_id})
        return [dict(row._mapping) for row in result]
