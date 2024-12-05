from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text


class InterviewRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_interviews_by_candidate(self, candidate_id: int):
        query = text("""
                    SELECT 
                        i.id,
                        i.interview_result,
                        v.description,
                        v.requirements,
                        v.publication_date,
                        p.title AS position_title,
                        e.company_name
                    FROM interviews i
                    JOIN vacancies v ON i.vacancy_id = v.id
                    JOIN positions p ON v.position_id = p.id
                    JOIN employers e ON v.employer_id = e.id
                    WHERE i.candidate_id = :candidate_id
                    ORDER BY 
                        CASE 
                            WHEN i.interview_result IS NULL THEN 0
                            WHEN i.interview_result = TRUE THEN 1
                            ELSE 2
                        END
                """)
        result = await self.db_session.execute(query,
                                               {"candidate_id": candidate_id})
        return [dict(row._mapping) for row in result]
