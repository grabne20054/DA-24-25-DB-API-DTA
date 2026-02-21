from fastapi import APIRouter, Depends

from crud import crud
from api.model import Customer, CustomerDB
from uuid import UUID
from api.check_req_type import allow_get_only
from api.dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter(dependencies=[Depends(allow_get_only)])

@router.post("/customers/", response_model=CustomerDB, status_code=201)
async def create_customer(payload: Customer, db: Session = Depends(get_db)):
    customer_id = crud.create_customer(payload, db)

    response_object = {
        "customerId": customer_id,
        "firstName": payload.firstName,
        "lastName": payload.lastName,
        "email": payload.email,
        "password": payload.password,
        "phoneNumber": payload.phoneNumber,
        "companyNumber": payload.companyNumber,
        "customerReference": payload.customerReference,
        "signedUp": payload.signedUp,
        "role": payload.role,
        "businessSector": payload.businessSector,
        "avatarPath": payload.avatarPath,
        "addressId": payload.addressId,
        "deleted": payload.deleted,
        "modifiedAt": payload.modifiedAt
    }
    return response_object


@router.get("/customers/{customer_id}/", response_model=CustomerDB, status_code=200)
async def read_customer(customer_id: UUID, db: Session = Depends(get_db)):
    customer = crud.get_customer(customer_id, db)
    return customer

@router.delete("/customers/{customer_id}/", status_code=200)
async def delete_customer(customer_id: UUID, db: Session = Depends(get_db)):
    customer = crud.delete_customer(customer_id, db)
    return customer

@router.get("/customers/", status_code=200)
async def read_customers(db: Session = Depends(get_db)):
    customers = crud.get_customers(db)
    return customers

@router.delete("/customers/", status_code=200)
async def delete_customers(db: Session = Depends(get_db)):
    crud.delete_customers(db)
    return True
