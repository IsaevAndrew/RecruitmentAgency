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

    async def get_pending_interviews_by_employer(self, employer_id: int):
        query = text("""
            SELECT 
                i.id,
                c.last_name,
                c.first_name,
                c.middle_name,
                c.city,
                c.email,
                c.phone,
                v.description,
                v.requirements,
                p.title AS position_title
            FROM interviews i
            JOIN candidates c ON i.candidate_id = c.id
            JOIN vacancies v ON i.vacancy_id = v.id
            JOIN positions p ON v.position_id = p.id
            WHERE v.employer_id = :employer_id AND i.interview_result IS NULL
        """)
        result = await self.db_session.execute(query,
                                               {"employer_id": employer_id})
        return [dict(row._mapping) for row in result]

    async def update_interview_result(self, interview_id: int, result: bool):
        query = text("""
            UPDATE interviews
            SET interview_result = :result
            WHERE id = :interview_id
        """)
        result = await self.db_session.execute(query, {"result": result,
                                                       "interview_id": interview_id})
        await self.db_session.commit()
        return result.rowcount > 0
