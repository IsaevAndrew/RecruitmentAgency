from app.db.repositories.positions import PositionRepository


class PositionService:
    def __init__(self, position_repo: PositionRepository):
        self.position_repo = position_repo

    async def fetch_all_positions(self):
        return await self.position_repo.get_all_positions()
