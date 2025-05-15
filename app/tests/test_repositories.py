import pytest
from unittest.mock import AsyncMock, MagicMock

from app.db.repositories.candidates import CandidateRepository
from app.db.repositories.auth import AuthRepository
from app.db.repositories.applications import ApplicationRepository
from app.db.repositories.positions import PositionRepository
from app.db.repositories.contracts import ContractRepository
from app.db.repositories.vacancies import VacancyRepository
from app.db.repositories.employers import EmployerRepository
from app.db.repositories.interviews import InterviewRepository


@pytest.fixture
def mock_session():
    session = MagicMock()
    session.execute = AsyncMock()
    session.commit = AsyncMock()
    return session


# CandidateRepository

@pytest.mark.asyncio
async def test_candidate_is_email_taken_true(mock_session):
    mock_res = MagicMock()
    mock_res.scalar.return_value = 1
    mock_session.execute.return_value = mock_res
    repo = CandidateRepository(mock_session)
    assert await repo.is_email_taken("a@b") is True


@pytest.mark.asyncio
async def test_candidate_is_email_taken_false(mock_session):
    mock_res = MagicMock()
    mock_res.scalar.return_value = None
    mock_session.execute.return_value = mock_res
    repo = CandidateRepository(mock_session)
    assert await repo.is_email_taken("a@b") is False


@pytest.mark.asyncio
async def test_create_candidate(mock_session):
    data = {
        "last_name": "L", "first_name": "F", "middle_name": "M",
        "date_of_birth": "1990-01-01", "email": "e", "phone": "p",
        "password": "pwd", "city": "C", "education": "E",
        "work_experience": "WE", "skills": "S"
    }
    mock_res = MagicMock()
    mock_res.scalar.return_value = 42
    mock_session.execute.return_value = mock_res
    repo = CandidateRepository(mock_session)
    assert await repo.create_candidate(data) == 42
    mock_session.execute.assert_awaited_once()
    mock_session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_candidate_by_id(mock_session):
    mock_res = MagicMock()
    mock_res.fetchone.return_value = ("1", "L", "F")
    mock_session.execute.return_value = mock_res
    repo = CandidateRepository(mock_session)
    assert await repo.get_candidate_by_id(1) == ("1", "L", "F")


@pytest.mark.asyncio
async def test_update_candidate(mock_session):
    repo = CandidateRepository(mock_session)
    await repo.update_candidate(1, {
        "date_of_birth": "1990", "city": "C",
        "education": "E", "work_experience": "WE", "skills": "S"
    })
    mock_session.execute.assert_awaited_once()
    mock_session.commit.assert_awaited_once()


# AuthRepository

@pytest.mark.asyncio
async def test_get_user_by_email(mock_session):
    mock_res = MagicMock()
    mock_res.fetchone.return_value = ("1", "e", "pwd")
    mock_session.execute.return_value = mock_res
    repo = AuthRepository(mock_session)
    assert await repo.get_user_by_email("e") == ("1", "e", "pwd")


@pytest.mark.asyncio
async def test_get_employer_by_email(mock_session):
    mock_res = MagicMock()
    mock_res.fetchone.return_value = ("2", "e", "pwd2")
    mock_session.execute.return_value = mock_res
    repo = AuthRepository(mock_session)
    assert await repo.get_employer_by_email("e") == ("2", "e", "pwd2")


# ApplicationRepository

@pytest.mark.asyncio
async def test_create_application(mock_session):
    repo = ApplicationRepository(mock_session)
    await repo.create_application(1, 2)
    mock_session.execute.assert_awaited_once()
    mock_session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_applications_by_candidate(mock_session):
    row1 = MagicMock();
    row1._mapping = {"id": 1, "vacancy_id": 2}
    row2 = MagicMock();
    row2._mapping = {"id": 3}
    mock_session.execute.return_value = [row1, row2]
    repo = ApplicationRepository(mock_session)
    assert await repo.get_applications_by_candidate(1) == [
        {"id": 1, "vacancy_id": 2}, {"id": 3}
    ]


# PositionRepository

@pytest.mark.asyncio
async def test_get_all_positions(mock_session):
    row1 = MagicMock();
    row1.id = 1;
    row1.title = "T1"
    row2 = MagicMock();
    row2.id = 2;
    row2.title = "T2"
    mock_res = MagicMock()
    mock_res.fetchall.return_value = [row1, row2]
    mock_session.execute.return_value = mock_res
    repo = PositionRepository(mock_session)
    assert await repo.get_all_positions() == [
        {"id": 1, "title": "T1"}, {"id": 2, "title": "T2"}
    ]


# ContractRepository

@pytest.mark.asyncio
async def test_get_contracts_by_candidate(mock_session):
    row = MagicMock();
    row._mapping = {"id": 1}
    mock_session.execute.return_value = [row]
    repo = ContractRepository(mock_session)
    assert await repo.get_contracts_by_candidate(1) == [{"id": 1}]


@pytest.mark.asyncio
async def test_get_contracts_by_employer(mock_session):
    row = MagicMock();
    row._mapping = {"id": 2}
    mock_session.execute.return_value = [row]
    repo = ContractRepository(mock_session)
    assert await repo.get_contracts_by_employer(1) == [{"id": 2}]


@pytest.mark.asyncio
async def test_create_contract(mock_session):
    repo = ContractRepository(mock_session)
    await repo.create_contract({
        "candidate_id": 1, "vacancy_id": 2, "employer_id": 3,
        "contract_date": "2025-01-01", "contract_end_date": "2026-01-01",
        "salary": 100, "contract_terms": "T"
    })
    mock_session.execute.assert_awaited_once()
    mock_session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_contract_true(mock_session):
    mock_res = MagicMock(rowcount=1)
    mock_session.execute.return_value = mock_res
    repo = ContractRepository(mock_session)
    assert await repo.delete_contract(1) is True


@pytest.mark.asyncio
async def test_delete_contract_false(mock_session):
    mock_res = MagicMock(rowcount=0)
    mock_session.execute.return_value = mock_res
    repo = ContractRepository(mock_session)
    assert await repo.delete_contract(1) is False


# VacancyRepository

@pytest.mark.asyncio
async def test_get_active_vacancies_no_filters(mock_session):
    row = MagicMock();
    row._mapping = {"id": 1}
    mock_session.execute.return_value = [row]
    repo = VacancyRepository(mock_session)
    assert await repo.get_active_vacancies() == [{"id": 1}]


@pytest.mark.asyncio
async def test_get_active_vacancies_with_filters(mock_session):
    row = MagicMock();
    row._mapping = {"id": 2}
    mock_session.execute.return_value = [row]
    repo = VacancyRepository(mock_session)
    assert await repo.get_active_vacancies(positions=[1],
                                           requirements="req") == [{"id": 2}]


@pytest.mark.asyncio
async def test_create_vacancy(mock_session):
    repo = VacancyRepository(mock_session)
    await repo.create_vacancy({
        "description": "D", "requirements": "R",
        "is_active": True, "employer_id": 1, "position_id": 1
    })
    mock_session.execute.assert_awaited_once()
    mock_session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_vacancy_status_true(mock_session):
    mock_res = MagicMock(rowcount=1)
    mock_session.execute.return_value = mock_res
    repo = VacancyRepository(mock_session)
    assert await repo.update_vacancy_status(1, True) is True


@pytest.mark.asyncio
async def test_update_vacancy_status_false(mock_session):
    mock_res = MagicMock(rowcount=0)
    mock_session.execute.return_value = mock_res
    repo = VacancyRepository(mock_session)
    assert await repo.update_vacancy_status(1, False) is False


@pytest.mark.asyncio
async def test_employer_is_email_taken_true(mock_session):
    mock_res = MagicMock()
    mock_res.scalar.return_value = 1
    mock_session.execute.return_value = mock_res
    repo = EmployerRepository(mock_session)
    assert await repo.is_email_taken("e") is True


@pytest.mark.asyncio
async def test_employer_is_email_taken_false(mock_session):
    mock_res = MagicMock()
    mock_res.scalar.return_value = None
    mock_session.execute.return_value = mock_res
    repo = EmployerRepository(mock_session)
    assert await repo.is_email_taken("e") is False


@pytest.mark.asyncio
async def test_create_employer(mock_session):
    mock_res = MagicMock()
    mock_res.scalar.return_value = 99
    mock_session.execute.return_value = mock_res
    repo = EmployerRepository(mock_session)
    assert await repo.create_employer({
        "email": "e", "phone": "p", "password": "pwd",
        "company_name": "C", "address": "A", "about_company": "AC"
    }) == 99


@pytest.mark.asyncio
async def test_get_employer_by_id(mock_session):
    mock_res = MagicMock()
    mock_res.fetchone.return_value = {"id": 1, "company_name": "C",
                                      "email": "e",
                                      "phone": "p", "address": "A",
                                      "about_company": "AC"}
    mock_session.execute.return_value = mock_res
    repo = EmployerRepository(mock_session)
    assert await repo.get_employer_by_id(1) == {
        "id": 1, "company_name": "C", "email": "e",
        "phone": "p", "address": "A", "about_company": "AC"
    }


@pytest.mark.asyncio
async def test_update_employer(mock_session):
    repo = EmployerRepository(mock_session)
    await repo.update_employer(1, {
        "company_name": "C", "email": "e",
        "phone": "p", "address": "A", "about_company": "AC"
    })
    mock_session.execute.assert_awaited_once()
    mock_session.commit.assert_awaited_once()


# InterviewRepository

@pytest.mark.asyncio
async def test_get_interviews_by_candidate(mock_session):
    row = MagicMock();
    row._mapping = {"id": 1}
    mock_session.execute.return_value = [row]
    repo = InterviewRepository(mock_session)
    assert await repo.get_interviews_by_candidate(1) == [{"id": 1}]


@pytest.mark.asyncio
async def test_get_pending_interviews_by_employer(mock_session):
    row = MagicMock();
    row._mapping = {"id": 2}
    mock_session.execute.return_value = [row]
    repo = InterviewRepository(mock_session)
    assert await repo.get_pending_interviews_by_employer(1) == [{"id": 2}]


@pytest.mark.asyncio
async def test_update_interview_result(mock_session):
    repo = InterviewRepository(mock_session)
    await repo.update_interview_result(1, True)
    mock_session.execute.assert_awaited_once()
    mock_session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_interview_by_id_none(mock_session):
    mock_res = MagicMock()
    mock_res.fetchone.return_value = None
    mock_session.execute.return_value = mock_res
    repo = InterviewRepository(mock_session)
    assert await repo.get_interview_by_id(1) is None
