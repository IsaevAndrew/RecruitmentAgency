from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request, Form
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.db.dependencies import get_db
from app.services.session_service import get_current_user
from app.services.contract_service import ContractService

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get(
    "/",
    tags=["contracts"],
    summary="Контракт по id",
    description="Позволяет получить информацию по котракту"
)
async def get_contracts(
        request: Request,
        db: AsyncSession = Depends(get_db)
):
    current_user = get_current_user(request)
    service = ContractService(db)
    if current_user["role"] == "candidate":
        contracts = await service.get_contracts_by_candidate(
            candidate_id=current_user["user_id"]
        )
        return templates.TemplateResponse(
            "candidate_contracts.html",
            {"request": request, "contracts": contracts}
        )
    elif current_user["role"] == "employer":
        contracts = await service.get_contracts_by_employer(
            employer_id=current_user["user_id"]
        )
        return templates.TemplateResponse(
            "employer_contracts.html",
            {"request": request, "contracts": contracts}
        )
    else:
        raise HTTPException(status_code=403, detail="Доступ запрещен")


@router.post(
    "/create",
    tags=["contracts"],
    summary="Создание контракта",
    description="Создает новый контракт между кандидатом и работодателем"
)
async def create_contract(
        candidate_id: int = Form(..., description="ID кандидата"),
        vacancy_id: int = Form(..., description="ID вакансии"),
        employer_id: int = Form(..., description="ID работодателя"),
        contract_date: str = Form(...,
                                  description="Дата начала контракта (YYYY-MM-DD)"),
        contract_end_date: str = Form(...,
                                      description="Дата окончания контракта (YYYY-MM-DD)"),
        salary: int = Form(..., description="Зарплата по контракту"),
        contract_terms: str = Form(..., description="Условия контракта"),
        db: AsyncSession = Depends(get_db)
):
    contract_date_obj = datetime.strptime(contract_date, "%Y-%m-%d").date()
    contract_end_date_obj = datetime.strptime(contract_end_date,
                                              "%Y-%m-%d").date()

    service = ContractService(db)
    await service.create_contract(
        candidate_id=candidate_id,
        vacancy_id=vacancy_id,
        employer_id=employer_id,
        contract_date=contract_date_obj,
        contract_end_date=contract_end_date_obj,
        salary=salary,
        contract_terms=contract_terms,
    )

    return RedirectResponse(url="/contracts", status_code=303)


@router.delete(
    "/{contract_id}",
    tags=["contracts"],
    summary="Удаление контракта",
    description="Удаляет контракт по его идентификатору"
)
async def delete_contract(
        contract_id: int,
        db: AsyncSession = Depends(get_db)
):
    service = ContractService(db)
    success = await service.delete_contract(contract_id)
    if not success:
        raise HTTPException(status_code=404, detail="Контракт не найден")
    return {"message": "Контракт успешно удален"}
