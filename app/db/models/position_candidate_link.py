from sqlalchemy import Column, Integer, ForeignKey
from app.db.database import Base


class PositionCandidateLink(Base):
    __tablename__ = 'position_candidate_link'

    position_id = Column(Integer, ForeignKey('positions.id'), primary_key=True)
    candidate_id = Column(Integer, ForeignKey('candidates.id'), primary_key=True)
