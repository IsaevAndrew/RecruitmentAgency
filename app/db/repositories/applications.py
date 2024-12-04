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
