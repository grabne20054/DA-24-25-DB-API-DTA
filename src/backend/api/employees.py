from fastapi import APIRouter, Depends

from api.model import Employee, EmployeeDB
from crud import crud
from uuid import UUID
from api.check_req_type import allow_get_only
from api.dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/employees/", response_model=EmployeeDB, status_code=201)
async def create_employee(payload: Employee, db: Session = Depends(get_db)):
    employee_id = crud.create_employee(payload, db)

    response_object = {
        "employeeId": employee_id,
        "firstName": payload.firstName,
        "lastName": payload.lastName,
        "password": payload.password,
        "email": payload.email,
        "roleId": payload.roleId,
        "deleted": payload.deleted,
    }
    return response_object

@router.get("/employees/{employee_id}/", response_model=EmployeeDB, status_code=200)
async def read_employee(employee_id: UUID, db: Session = Depends(get_db)):
    employee = crud.get_employee(employee_id, db)
    return employee


@router.delete("/employees/{employee_id}/", status_code=200)
async def delete_employee(employee_id: UUID, db: Session = Depends(get_db)):
    employee = crud.delete_employee(employee_id, db)
    return employee

@router.get("/employees/", status_code=200)
async def read_employees(email:str = None, password:str = None, db: Session = Depends(get_db)):
    employees = crud.get_employees(email, password, db)
    return employees

@router.delete("/employees/", status_code=200)
async def delete_employees():
    crud.delete_employees()
    return True