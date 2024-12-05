import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.sql import text
from app.consts import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
import asyncio

# Подключение к базе данных
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_async_engine(DATABASE_URL, echo=True)


def create_database():
    """
    Создает базу данных, если она не существует.
    """
    try:
        # Подключаемся к PostgreSQL без указания базы данных
        connection = psycopg2.connect(
            dbname="postgres",
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()

        # Проверяем, существует ли база данных
        cursor.execute(
            f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DB_NAME}';"
        )
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(f"CREATE DATABASE {DB_NAME};")
            print(f"База данных '{DB_NAME}' создана.")
        else:
            print(f"База данных '{DB_NAME}' уже существует.")

        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Ошибка при создании базы данных: {e}")


# Список SQL-запросов для создания таблиц
TABLE_CREATION_QUERIES = [
    text("""
    DO $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'gender_enum') THEN
            CREATE TYPE gender_enum AS ENUM ('мужчина', 'женщина');
        END IF;
    END $$;
    """),
    text("""
        CREATE TABLE IF NOT EXISTS employers (
            id SERIAL PRIMARY KEY,
            company_name VARCHAR(255) NOT NULL,
            address VARCHAR(255),
            about_company TEXT,
            email VARCHAR(255) UNIQUE NOT NULL,
            phone VARCHAR(20),
            password VARCHAR(255) NOT NULL
        );
        """),
    text("""
        CREATE TABLE IF NOT EXISTS candidates (
            id SERIAL PRIMARY KEY,
            last_name VARCHAR(100) NOT NULL,
            first_name VARCHAR(100) NOT NULL,
            middle_name VARCHAR(100),
            date_of_birth DATE,
            gender gender_enum NOT NULL,
            city VARCHAR(100),
            phone VARCHAR(20),
            email VARCHAR(255) UNIQUE NOT NULL,
            education TEXT,
            work_experience TEXT,
            skills TEXT,
            password VARCHAR(255) NOT NULL
        );
        """),
    text("""
    CREATE TABLE IF NOT EXISTS positions (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL
    );
    """),
    text("""
    CREATE TABLE IF NOT EXISTS vacancies (
        id SERIAL PRIMARY KEY,
        description TEXT,
        requirements TEXT,
        publication_date TIMESTAMP NOT NULL DEFAULT NOW(),
        is_active BOOLEAN NOT NULL DEFAULT TRUE,
        employer_id INT REFERENCES employers(id) ON DELETE CASCADE,
        position_id INT REFERENCES positions(id) ON DELETE SET NULL
    );
    """),
    text("""
    CREATE TABLE IF NOT EXISTS contracts (
        id SERIAL PRIMARY KEY,
        candidate_id INT REFERENCES candidates(id) ON DELETE CASCADE,
        vacancy_id INT REFERENCES vacancies(id) ON DELETE CASCADE,
        contract_date DATE NOT NULL,
        contract_status VARCHAR(50) NOT NULL
    );
    """),
    text("""
    CREATE TABLE IF NOT EXISTS interviews (
        id SERIAL PRIMARY KEY,
        candidate_id INT REFERENCES candidates(id) ON DELETE CASCADE,
        vacancy_id INT REFERENCES vacancies(id) ON DELETE CASCADE,
        interview_result BOOLEAN DEFAULT NULL
    );
    """),
    text("""
    CREATE TABLE IF NOT EXISTS job_applications (
        id SERIAL PRIMARY KEY,
        candidate_id INT REFERENCES candidates(id) ON DELETE CASCADE,
        vacancy_id INT REFERENCES vacancies(id) ON DELETE CASCADE,
        application_date TIMESTAMP NOT NULL
    );
    """),
    text("""
    CREATE TABLE IF NOT EXISTS position_candidate_link (
        position_id INT REFERENCES positions(id) ON DELETE CASCADE,
        candidate_id INT REFERENCES candidates(id) ON DELETE CASCADE,
        PRIMARY KEY (position_id, candidate_id)
    );
    """),
    text("""
    CREATE OR REPLACE FUNCTION create_interview()
    RETURNS TRIGGER AS $$
    BEGIN
        INSERT INTO interviews (candidate_id, vacancy_id, interview_result)
        VALUES (NEW.candidate_id, NEW.vacancy_id, NULL);
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """),
    text("""
    CREATE OR REPLACE TRIGGER after_job_application_insert
    AFTER INSERT ON job_applications
    FOR EACH ROW
    EXECUTE FUNCTION create_interview();
    """)
]

POSITIONS = [
    {"title": "Junior Python Developer"},
    {"title": "Middle Python Developer"},
    {"title": "Senior Python Developer"},
    {"title": "Junior Java Developer"},
    {"title": "Middle Java Developer"},
    {"title": "Senior Java Developer"},
    {"title": "Junior Frontend Developer"},
    {"title": "Middle Frontend Developer"},
    {"title": "Senior Frontend Developer"},
    {"title": "Junior DevOps Engineer"},
    {"title": "Middle DevOps Engineer"},
    {"title": "Senior DevOps Engineer"},
    {"title": "Data Scientist"},
    {"title": "Data Engineer"},
    {"title": "Game Developer"},
    {"title": "Mobile Developer (iOS)"},
    {"title": "Mobile Developer (Android)"},
    {"title": "Junior QA Engineer"},
    {"title": "Middle QA Engineer"},
    {"title": "Senior QA Engineer"},
    {"title": "Junior Go Developer"},
    {"title": "Middle Go Developer"},
    {"title": "Senior Go Developer"},
    {"title": "Business Analyst"},
    {"title": "System Analyst"},
    {"title": "Product Manager"},
    {"title": "Project Manager"},
    {"title": "Team Lead"},
    {"title": "Technical Director"},
    {"title": "CTO (Chief Technology Officer)"}
]


async def execute_sql(sql: text):
    """
    Выполняет SQL-запрос через асинхронное подключение.
    """
    async with engine.connect() as conn:
        await conn.execute(sql)
        await conn.commit()


async def populate_positions():
    """
    Проверяет и заполняет таблицу positions, если она пуста.
    """
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT COUNT(*) FROM positions"))
        count = result.scalar()
        if count == 0:
            for position in POSITIONS:
                await conn.execute(
                    text("INSERT INTO positions (title) VALUES (:title)"),
                    position,
                )
            await conn.commit()
            print("Таблица 'positions' успешно заполнена.")
        else:
            print("Таблица 'positions' уже содержит данные.")


async def create_tables():
    """
    Создает все таблицы и триггеры в базе данных.
    """
    try:
        for query in TABLE_CREATION_QUERIES:
            await execute_sql(query)
        await populate_positions()
        print("Создание таблиц прошло успешно.")
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")


if __name__ == "__main__":
    create_database()
    asyncio.run(create_tables())
