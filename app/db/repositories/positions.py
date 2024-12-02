from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text


class PositionRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all_positions(self):
        query = text("SELECT id, title FROM positions")
        result = await self.db_session.execute(query)
        return [{"id": row.id, "title": row.title} for row in result.fetchall()]
