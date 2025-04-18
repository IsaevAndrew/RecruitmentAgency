# Recruitment Agency Web Application

## **Описание**
Recruitment Agency — это веб-приложение, разработанное для автоматизации процесса взаимодействия между работодателями и кандидатами. Основные возможности приложения включают размещение вакансий, отклики кандидатов, управление собеседованиями и создание контрактов. Оно предоставляет простой и интуитивно понятный интерфейс как для кандидатов, так и для работодателей.

## **Стэк технологий**
- **Backend:** Python, FastAPI
- **Frontend:** HTML, CSS, JavaScript
- **База данных:** PostgreSQL, SQLAlchemy (асинхронный режим с использованием AsyncSession)
- **Контейнеризация:** Docker, Docker Compose
- **Дополнительно:** Jinja2 для шаблонизации страниц, асинхронные запросы на клиенте с использованием Fetch API

## **Мануал по запуску**
### **Предварительные требования**
- Установленный Docker и Docker Compose
- Клонированный репозиторий:
  ```bash
  git clone https://github.com/IsaevAndrew/RecruitmentAgency.git
  cd RecruitmentAgency
  ```

### **Запуск проекта**
1. **Настройка переменных окружения**
   В корне проекта находятся файлы `.env.local` и `.env.prod`. Проверьте его и убедитесь, что значения настроены корректно:
   ```dotenv
   DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
   ```

2. **Запуск Docker Compose**
   Выполните следующую команду для запуска контейнеров:
   ```bash
   docker-compose -f docker-compose.local.yml --env-file .env.local up --build
   ```

3. **Доступ к приложению**
   После успешного запуска приложение будет доступно по адресу:
   ```
   http://localhost:8000
   ```

### **Функциональные возможности**
- **Кандидаты**:
  - Регистрация и авторизация.
  - Просмотр списка вакансий.
  - Оставление откликов на вакансии.
  - Просмотр собеседований и заключенных контрактов.

- **Работодатели**:
  - Создание и управление вакансиями.
  - Просмотр откликов и проведение собеседований.
  - Заключение контрактов с кандидатами.

- **Общие возможности**:
  - Удобный интерфейс для управления контентом.
  - Реализована валидация данных на клиенте и сервере.

### **Контейнеризация**
Docker Compose файл включает:
- **PostgreSQL:** база данных для хранения информации.
- **Приложение FastAPI:** серверная часть приложения.

## **Особенности проекта**
1. **Ролевая система**:
   - Поддерживаются роли "Кандидат" и "Работодатель", каждая из которых имеет доступ к своим уникальным возможностям.

2. **Валидация данных**:
   - Реализована клиентская и серверная проверка введенных данных, включая даты, почту, телефон и пароли.

3. **Асинхронность**:
   - Использование асинхронного взаимодействия между сервером и клиентом для повышения производительности.

4. **UI/UX**:
   - Динамические элементы интерфейса, например, автоматическое включение кнопки "Сохранить", когда все поля формы заполнены корректно.

5. **Контейнеризация**:
   - Упрощенный процесс развертывания благодаря Docker Compose.
