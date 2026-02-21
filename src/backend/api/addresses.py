from fastapi import APIRouter, Depends
from api.model import Address, AddressDB
from crud import crud

from uuid import UUID
from api.check_req_type import allow_get_only
from api.dependencies import get_db
from sqlalchemy.orm import Session


router = APIRouter(dependencies=[Depends(allow_get_only)])

@router.post("/addresses/", response_model=AddressDB, status_code=201)
async def create_address(payload: Address, db: Session = Depends(get_db)):
    address_id = crud.create_address(payload, db)

    response_object = {
        "addressId": address_id,
        "streetName": payload.streetName,
        "streetNumber": payload.streetNumber,
        "city": payload.city,
        "postCode": payload.postCode,
        "country": payload.country,
        "state": payload.state,
        "deleted": payload.deleted,
        "modifiedAt":payload.modifiedAt

    }
    return response_object

@router.get("/addresses/{address_id}/", response_model=AddressDB, status_code=200)
async def read_address(address_id: UUID, db: Session = Depends(get_db)):
    address = crud.get_address(address_id, db)
    return address

@router.delete("/addresses/{address_id}/", status_code=200)
async def delete_address(address_id: UUID, db: Session = Depends(get_db)):
    address_id = crud.delete_address(address_id, db)
    return address_id

@router.get("/addresses/", status_code=200)
async def read_addresses(db: Session = Depends(get_db)):
    addresses = crud.get_addresses(db)
    return addresses

@router.delete("/addresses/", status_code=200)
async def delete_addresses(db: Session = Depends(get_db)):
    crud.delete_addresses(db)
    return True