from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.db.repositories.applications import ApplicationRepository


class ApplicationService:
    def __init__(self, repo: ApplicationRepository):
        self.repo = repo

    async def create_application(self, candidate_id: int, vacancy_id: int):
        try:
            return await self.repo.create_application(candidate_id, vacancy_id)
        except IntegrityError:
            raise ValueError("Вы уже откликнулись на эту вакансию.")

    async def get_applications_by_candidate(self, candidate_id: int):
        return await self.repo.get_applications_by_candidate(candidate_id)
