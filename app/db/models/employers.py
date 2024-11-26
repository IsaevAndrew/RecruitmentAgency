from sqlalchemy import Column, Integer, String
from app.db.database import Base


class Employer(Base):
    __tablename__ = 'employers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=True)
    about_company = Column(String(255), nullable=True)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20), nullable=True)
    password = Column(String(255), nullable=False)
