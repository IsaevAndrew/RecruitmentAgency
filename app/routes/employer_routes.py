from fastapi import APIRouter, Form, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.employer_service import EmployerService
from app.db.repositories.employers import EmployerRepository
from app.db.dependencies import get_db

router = APIRouter()


@router.post("/employer")
async def register_employer(
        email: str = Form(...),
        phone: str = Form(...),
        password: str = Form(...),
        confirm_password: str = Form(...),
        company_name: str = Form(...),
        address: str = Form(...),
        about_company: str = Form(None),
        db: AsyncSession = Depends(get_db)
):
    service = EmployerService(repo=EmployerRepository(db_session=db))
    employer_data = {
        "email": email,
        "phone": phone,
        "password": password,
        "confirm_password": confirm_password,
        "company_name": company_name,
        "address": address,
        "about_company": about_company,
    }

    try:
        employer_id = await service.create_employer(employer_data)
        return {"status": "success", "employer_id": employer_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
