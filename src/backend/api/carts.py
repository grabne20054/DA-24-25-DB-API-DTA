from fastapi import APIRouter, Depends


from crud import crud
from api.model import Cart, CartDB
from uuid import UUID
from api.check_req_type import allow_get_only


router = APIRouter(dependencies=[Depends(allow_get_only)])

@router.post("/carts/", response_model=CartDB, status_code=201)
async def create_cart(payload: Cart):
    cart_id = crud.create_cart(payload)

    response_object = {
        "cartId": cart_id,
        "customerReference": payload.customerReference,
    }
    return response_object


@router.get("/carts/{cart_id}/", response_model=CartDB, status_code=200)
async def read_cart(cart_id: UUID):
    cart = crud.get_cart(cart_id)
    return cart

@router.delete("/carts/{cart_id}/", status_code=200)
async def delete_cart(cart_id: UUID):
    cart = crud.delete_cart(cart_id)
    return cart

@router.get("/carts/", status_code=200)
async def read_carts():
    carts = crud.get_carts()
    return carts

@router.delete("/carts/", status_code=200)
async def delete_carts():
    crud.delete_carts()
    return True
