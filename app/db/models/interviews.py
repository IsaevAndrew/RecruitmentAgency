from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text
from app.db.database import Base


class Interview(Base):
    __tablename__ = 'interviews'

    id = Column(Integer, primary_key=True, autoincrement=True)
    verdict = Column(Text, nullable=True)
    employer_id = Column(Integer, ForeignKey('employers.id'), nullable=False)
    candidate_id = Column(Integer, ForeignKey('candidates.id'), nullable=False)
    vacancy_id = Column(Integer, ForeignKey('vacancies.id'), nullable=False)
