from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text


class ContractRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_contracts_by_candidate(self, candidate_id: int):
        query = text("""
            SELECT 
                c.id,
                c.contract_date,
                c.contract_end_date,
                c.salary,
                c.contract_terms,
                v.description,
                v.requirements,
                v.publication_date,
                p.title AS position_title,
                e.company_name
            FROM contracts c
            JOIN vacancies v ON c.vacancy_id = v.id
            JOIN positions p ON v.position_id = p.id
            JOIN employers e ON c.employer_id = e.id
            WHERE c.candidate_id = :candidate_id
            ORDER BY c.contract_date DESC
        """)
        result = await self.db_session.execute(query,
                                               {"candidate_id": candidate_id})
        return [dict(row._mapping) for row in result]

    async def get_contracts_by_employer(self, employer_id: int):
        query = text("""
            SELECT 
                c.id,
                c.contract_date,
                c.contract_end_date,
                c.salary,
                c.contract_terms,
                v.description AS vacancy_description,
                v.requirements AS vacancy_requirements,
                v.publication_date AS vacancy_publication_date,
                p.title AS position_title,
                e.company_name AS employer_name,
                can.first_name AS candidate_first_name,
                can.last_name AS candidate_last_name,
                can.middle_name AS candidate_middle_name,
                can.email AS candidate_email,
                can.phone AS candidate_phone,
                can.city AS candidate_city
            FROM contracts c
            JOIN vacancies v ON c.vacancy_id = v.id
            JOIN positions p ON v.position_id = p.id
            JOIN employers e ON c.employer_id = e.id
            JOIN candidates can ON c.candidate_id = can.id
            WHERE c.employer_id = :employer_id
            ORDER BY c.contract_date DESC
        """)
        result = await self.db_session.execute(query,
                                               {"employer_id": employer_id})
        return [dict(row._mapping) for row in result]

    async def create_contract(self, contract_data: dict):
        query = text("""
            INSERT INTO contracts (
                candidate_id, vacancy_id, employer_id, contract_date,
                contract_end_date, salary, contract_terms
            ) VALUES (
                :candidate_id, :vacancy_id, :employer_id, :contract_date,
                :contract_end_date, :salary, :contract_terms
            )
        """)
        await self.db_session.execute(query, contract_data)
        await self.db_session.commit()

    async def delete_contract(self, contract_id: int) -> bool:
        query = text("DELETE FROM contracts WHERE id = :contract_id")
        result = await self.db_session.execute(query,
                                               {"contract_id": contract_id})
        await self.db_session.commit()
        return result.rowcount > 0