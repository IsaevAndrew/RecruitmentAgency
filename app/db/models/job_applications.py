from sqlalchemy import Column, Integer, ForeignKey, DateTime
from app.db.database import Base


class JobApplication(Base):
    __tablename__ = 'job_applications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    submission_date = Column(DateTime, nullable=False)
    candidate_id = Column(Integer, ForeignKey('candidates.id'), nullable=False)
    vacancy_id = Column(Integer, ForeignKey('vacancies.id'), nullable=False)
