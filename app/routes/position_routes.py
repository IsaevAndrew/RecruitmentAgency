from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.dependencies import get_db
from app.services.position_service import PositionService
from app.db.repositories.positions import PositionRepository

router = APIRouter()


@router.get("/positions")
async def get_positions(db: AsyncSession = Depends(get_db)):
    """
    Возвращает список позиций через сервис.
    """
    position_repo = PositionRepository(db)
    position_service = PositionService(position_repo)
    positions = await position_service.fetch_all_positions()
    return {"positions": positions}