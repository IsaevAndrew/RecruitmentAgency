from app.db.repositories.interviews import InterviewRepository


class InterviewService:
    def __init__(self, db_session):
        self.repo = InterviewRepository(db_session)

    async def get_interviews_by_candidate(self, candidate_id: int):
        return await self.repo.get_interviews_by_candidate(candidate_id)

    async def get_pending_interviews_by_employer(self, employer_id: int):
        return await self.repo.get_pending_interviews_by_employer(employer_id)

    async def update_interview_result(self, interview_id: int, result: bool):
        return await self.repo.update_interview_result(interview_id, result)

    async def get_interview_by_id(self, interview_id: int):
        return await self.repo.get_interview_by_id(interview_id)
