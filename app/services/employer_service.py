import bcrypt
from app.db.repositories.employers import EmployerRepository


class EmployerService:
    def __init__(self, repo: EmployerRepository):
        self.repo = repo

    async def create_employer(self, employer_data: dict):
        if await self.repo.is_email_taken(employer_data["email"]):
            raise ValueError("Email уже зарегистрирован")
        if employer_data["password"] != employer_data["confirm_password"]:
            raise ValueError("Пароли не совпадают")
        hashed_password = bcrypt.hashpw(
            employer_data["password"].encode('utf-8'), bcrypt.gensalt()
        )
        employer_data["password"] = hashed_password.decode('utf-8')
        del employer_data["confirm_password"]
        return await self.repo.create_employer(employer_data)

    async def get_employer_profile(self, employer_id: int):
        """
        Получить профиль работодателя по его ID.
        """
        return await self.repo.get_employer_by_id(employer_id)

    async def update_employer_profile(self, employer_id: int,
                                      updated_data: dict):
        """
        Обновить профиль работодателя.
        """
        await self.repo.update_employer(employer_id, updated_data)
