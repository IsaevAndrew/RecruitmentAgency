from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text, Boolean
from app.db.database import Base


class Vacancy(Base):
    __tablename__ = 'vacancies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(Text, nullable=True)  # Описание вакансии
    requirements = Column(Text, nullable=True)  # Требования
    publication_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    is_active = Column(Boolean, nullable=False, default=True)  # Активность вакансии
    employer_id = Column(Integer, ForeignKey('employers.id'), nullable=False)  # Работодатель
    position_id = Column(Integer, ForeignKey('positions.id'), nullable=False)  # Позиция

