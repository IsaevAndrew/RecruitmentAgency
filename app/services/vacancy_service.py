from app.db.repositories.vacancies import VacancyRepository


class VacancyService:
    def __init__(self, repo: VacancyRepository):
        self.repo = repo

    async def get_active_vacancies(self, positions=None, requirements=None):
        return await self.repo.get_active_vacancies(positions, requirements)

    async def create_vacancy(self, vacancy_data: dict):
        await self.repo.create_vacancy(vacancy_data)

    async def deactivate_vacancy(self, vacancy_id: int) -> bool:
        return await self.repo.update_vacancy_status(vacancy_id,
                                                     is_active=False)

    async def activate_vacancy(self, vacancy_id: int) -> bool:
        return await self.repo.update_vacancy_status(vacancy_id, is_active=True)

    async def filter_vacancies(self, positions,
                               requirements):
        return await self.repo.filter_vacancies(positions, requirements)

    async def get_vacancy_by_id(self, vacancy_id: int):
        return await self.repo.get_vacancy_by_id(vacancy_id)

    async def get_vacancies_with_application_status(self, candidate_id: int,
                                                    positions=None,
                                                    requirements=None):
        return await self.repo.get_vacancies_with_application_status(
            candidate_id, positions, requirements)
