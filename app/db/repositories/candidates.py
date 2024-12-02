from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text


class CandidateRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def is_email_taken(self, email: str) -> bool:
        query = text("SELECT 1 FROM candidates WHERE email = :email")
        result = await self.db_session.execute(query, {"email": email})
        return result.scalar() is not None

    async def create_candidate(self, candidate_data: dict):
        query = text("""
            INSERT INTO candidates (last_name, first_name, middle_name, date_of_birth, gender, email, phone, password, city, education, work_experience, skills)
            VALUES (:last_name, :first_name, :middle_name, :date_of_birth, :gender, :email, :phone, :password, :city, :education, :work_experience, :skills)
            RETURNING id;
        """)
        result = await self.db_session.execute(query, candidate_data)
        await self.db_session.commit()
        return result.scalar()

    async def get_candidate_by_id(self, candidate_id: int):
        query = text("""
            SELECT id, last_name, first_name, middle_name, date_of_birth, 
                   city, phone, email, education, work_experience, skills 
            FROM candidates
            WHERE id = :candidate_id
        """)
        result = await self.db_session.execute(query,
                                               {"candidate_id": candidate_id})
        return result.fetchone()

    async def update_candidate(self, candidate_id: int, updated_data: dict):
        query = text("""
            UPDATE candidates
            SET 
                date_of_birth = :date_of_birth,
                city = :city,
                education = :education,
                work_experience = :work_experience,
                skills = :skills
            WHERE id = :candidate_id
        """)
        await self.db_session.execute(query, {**updated_data,
                                              "candidate_id": candidate_id})
        await self.db_session.commit()
