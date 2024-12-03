from app.db.repositories.vacancies import VacancyRepository


class VacancyService:
    def __init__(self, repo: VacancyRepository):
        self.repo = repo

    async def get_active_vacancies(self):
        return await self.repo.get_active_vacancies()

    async def create_vacancy(self, vacancy_data: dict):
        await self.repo.create_vacancy(vacancy_data)

    async def deactivate_vacancy(self, vacancy_id: int) -> bool:
        return await self.repo.update_vacancy_status(vacancy_id,
                                                     is_active=False)

    async def activate_vacancy(self, vacancy_id: int) -> bool:
        return await self.repo.update_vacancy_status(vacancy_id, is_active=True)
