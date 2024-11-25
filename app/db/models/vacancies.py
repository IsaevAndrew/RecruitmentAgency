from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text
from app.db.database import Base



class Vacancy(Base):
    __tablename__ = 'vacancies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    requirements = Column(Text, nullable=True)
    publication_date = Column(DateTime, nullable=False)
    employer_id = Column(Integer, ForeignKey('employers.id'), nullable=False)
    position_id = Column(Integer, ForeignKey('positions.id'), nullable=False)
