from datetime import datetime, date
from app.db.repositories.candidates import CandidateRepository
import bcrypt


class CandidateService:
    def __init__(self, repo: CandidateRepository):
        self.repo = repo

    async def create_candidate(self, candidate_data: dict):
        if await self.repo.is_email_taken(candidate_data["email"]):
            raise ValueError("Email уже зарегистрирован")
        if candidate_data["password"] != candidate_data["confirm_password"]:
            raise ValueError("Пароли не совпадают")
        hashed_password = bcrypt.hashpw(
            candidate_data["password"].encode('utf-8'), bcrypt.gensalt()
        )
        candidate_data["password"] = hashed_password.decode('utf-8')
        del candidate_data["confirm_password"]
        if isinstance(candidate_data["date_of_birth"], str):
            candidate_data["date_of_birth"] = datetime.strptime(
                candidate_data["date_of_birth"], "%Y-%m-%d"
            ).date()

        gender_map = {"male": "мужчина", "female": "женщина"}
        candidate_data["gender"] = gender_map.get(candidate_data["gender"],
                                                  candidate_data["gender"])
        return await self.repo.create_candidate(candidate_data)

    async def get_candidate_profile(self, candidate_id: int):
        return await self.repo.get_candidate_by_id(candidate_id)

    async def update_candidate_profile(self, candidate_id: int,
                                       updated_data: dict):
        await self.repo.update_candidate(candidate_id, updated_data)
