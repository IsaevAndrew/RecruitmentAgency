from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float, Text
from app.db.database import Base


class Contract(Base):
    __tablename__ = 'contracts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    terms = Column(Text, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    salary = Column(Float, nullable=False)
    employer_id = Column(Integer, ForeignKey('employers.id'), nullable=False)
    candidate_id = Column(Integer, ForeignKey('candidates.id'), nullable=False)
    vacancy_id = Column(Integer, ForeignKey('vacancies.id'), nullable=False)
