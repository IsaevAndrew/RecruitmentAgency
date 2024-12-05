from app.db.repositories.interviews import InterviewRepository


class InterviewService:
    def __init__(self, db_session):
        self.repo = InterviewRepository(db_session)

    async def get_interviews_by_candidate(self, candidate_id: int):
        return await self.repo.get_interviews_by_candidate(candidate_id)
