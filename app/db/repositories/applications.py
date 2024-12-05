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
                v.id,
                v.description,
                v.requirements,
                v.publication_date,
                v.position_id,
                p.title AS position_title,
                e.company_name,
                ja.application_date
            FROM job_applications ja
            JOIN vacancies v ON ja.vacancy_id = v.id
            JOIN positions p ON v.position_id = p.id
            JOIN employers e ON v.employer_id = e.id
            WHERE ja.candidate_id = :candidate_id
            ORDER BY ja.application_date DESC
        """
        result = await self.db_session.execute(text(query),
                                               {"candidate_id": candidate_id})
        return [dict(row._mapping) for row in result]
