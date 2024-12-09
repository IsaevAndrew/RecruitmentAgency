from app.db.repositories.contracts import ContractRepository


class ContractService:
    def __init__(self, db_session):
        self.repo = ContractRepository(db_session)

    async def get_contracts_by_candidate(self, candidate_id: int):
        return await self.repo.get_contracts_by_candidate(candidate_id)

    async def get_contracts_by_employer(self, employer_id: int):
        return await self.repo.get_contracts_by_employer(employer_id)

    async def create_contract(self, candidate_id: int, vacancy_id: int,
                              employer_id: int,
                              contract_date: str, contract_end_date: str,
                              salary: int, contract_terms: str):
        await self.repo.create_contract({
            'candidate_id': candidate_id,
            'vacancy_id': vacancy_id,
            'employer_id': employer_id,
            'contract_date': contract_date,
            'contract_end_date': contract_end_date,
            'salary': salary,
            'contract_terms': contract_terms}
        )

    async def delete_contract(self, contract_id: int) -> bool:
        return await self.repo.delete_contract(contract_id)