from fastapi import APIRouter, Depends

from api.model import Employee, EmployeeDB
from crud import crud
from uuid import UUID
from api.check_req_type import allow_get_only

router = APIRouter()

@router.post("/employees/", response_model=EmployeeDB, status_code=201)
async def create_employee(payload: Employee):
    employee_id = crud.create_employee(payload)

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
async def read_employee(employee_id: UUID):
    employee = crud.get_employee(employee_id)
    return employee


@router.delete("/employees/{employee_id}/", status_code=200)
async def delete_employee(employee_id: UUID):
    employee = crud.delete_employee(employee_id)
    return employee

@router.get("/employees/", status_code=200)
async def read_employees(email:str = None, password:str = None):
    employees = crud.get_employees(email, password)
    return employees

@router.delete("/employees/", status_code=200)
async def delete_employees():
    crud.delete_employees()
    return True