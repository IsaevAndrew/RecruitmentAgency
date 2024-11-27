from datetime import datetime, date
from app.db.repositories.candidates import CandidateRepository
import bcrypt


class CandidateService:
    def __init__(self, repo: CandidateRepository):
        self.repo = repo

    async def create_candidate(self, candidate_data: dict):
        # Проверка, зарегистрирован ли email
        if await self.repo.is_email_taken(candidate_data["email"]):
            raise ValueError("Email уже зарегистрирован")

        # Проверка совпадения паролей
        if candidate_data["password"] != candidate_data["confirm_password"]:
            raise ValueError("Пароли не совпадают")

        # Хэширование пароля
        hashed_password = bcrypt.hashpw(
            candidate_data["password"].encode('utf-8'), bcrypt.gensalt()
        )
        candidate_data["password"] = hashed_password.decode('utf-8')
        del candidate_data["confirm_password"]

        # Преобразование даты рождения из строки в объект date
        if isinstance(candidate_data["date_of_birth"], str):
            candidate_data["date_of_birth"] = datetime.strptime(
                candidate_data["date_of_birth"], "%Y-%m-%d"
            ).date()

        # Преобразование значения gender
        gender_map = {"male": "мужчина", "female": "женщина"}
        candidate_data["gender"] = gender_map.get(candidate_data["gender"],
                                                  candidate_data["gender"])

        # Создание записи кандидата в базе данных
        return await self.repo.create_candidate(candidate_data)
