from fastapi import APIRouter

from api.model import Address, AddressDB
from crud import crud

from uuid import UUID


router = APIRouter()

@router.post("/addresses/", response_model=AddressDB, status_code=201)
async def create_address(payload: Address):
    address_id = crud.create_address(payload)

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
async def read_address(address_id: UUID):
    address = crud.get_address(address_id)
    return address

@router.delete("/addresses/{address_id}/", status_code=200)
async def delete_address(address_id: UUID):
    address_id = crud.delete_address(address_id)
    return address_id

@router.get("/addresses/", status_code=200)
async def read_addresses():
    addresses = crud.get_addresses()
    return addresses

@router.delete("/addresses/", status_code=200)
async def delete_addresses():
    crud.delete_addresses()
    return True