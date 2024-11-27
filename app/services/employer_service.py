import bcrypt
from app.db.repositories.employers import EmployerRepository


class EmployerService:
    def __init__(self, repo: EmployerRepository):
        self.repo = repo

    async def create_employer(self, employer_data: dict):
        # Проверка, зарегистрирован ли email
        if await self.repo.is_email_taken(employer_data["email"]):
            raise ValueError("Email уже зарегистрирован")

        # Проверка совпадения паролей
        if employer_data["password"] != employer_data["confirm_password"]:
            raise ValueError("Пароли не совпадают")

        # Хэширование пароля
        hashed_password = bcrypt.hashpw(
            employer_data["password"].encode('utf-8'), bcrypt.gensalt()
        )
        employer_data["password"] = hashed_password.decode('utf-8')
        del employer_data["confirm_password"]

        # Добавление работодателя в базу данных
        return await self.repo.create_employer(employer_data)
