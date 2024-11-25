from sqlalchemy import Column, Integer, String, Text, Date, Enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Candidate(Base):
    __tablename__ = 'candidates'

    id = Column(Integer, primary_key=True, autoincrement=True)
    last_name = Column(String(100), nullable=False)  # Фамилия
    first_name = Column(String(100), nullable=False)  # Имя
    middle_name = Column(String(100), nullable=True)  # Отчество (опционально)
    date_of_birth = Column(Date, nullable=True)  # Дата рождения
    gender = Column(Enum('мужчина', 'женщина', name='gender_enum'), nullable=False)  # Пол
    city = Column(String(100), nullable=True)  # Город проживания
    phone = Column(String(20), nullable=True)  # Телефон
    email = Column(String(255), unique=True, nullable=False)  # Электронная почта
    education = Column(Text, nullable=True)  # Образование
    work_experience = Column(Text, nullable=True)  # Опыт работы
    skills = Column(Text, nullable=True)  # Навыки
    password = Column(String(255), nullable=False)  # Пароль (хэшированный)
