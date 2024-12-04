from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.db.repositories.applications import ApplicationRepository


class ApplicationService:
    def __init__(self, db_session: AsyncSession):
        self.repo = ApplicationRepository(db_session)

    async def create_application(self, candidate_id: int, vacancy_id: int):
        try:
            return await self.repo.create_application(candidate_id, vacancy_id)
        except IntegrityError:
            raise ValueError("Вы уже откликнулись на эту вакансию.")
