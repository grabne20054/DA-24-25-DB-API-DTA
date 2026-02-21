from fastapi import APIRouter, Depends


from crud import crud
from api.model import Cart, CartDB
from uuid import UUID
from api.check_req_type import allow_get_only
from api.dependencies import get_db
from sqlalchemy.orm import Session


router = APIRouter(dependencies=[Depends(allow_get_only)])

@router.post("/carts/", response_model=CartDB, status_code=201)
async def create_cart(payload: Cart, db: Session = Depends(get_db)):
    cart_id = crud.create_cart(payload, db)

    response_object = {
        "cartId": cart_id,
        "customerReference": payload.customerReference,
    }
    return response_object


@router.get("/carts/{cart_id}/", response_model=CartDB, status_code=200)
async def read_cart(cart_id: UUID, db: Session = Depends(get_db)):
    cart = crud.get_cart(cart_id, db)
    return cart

@router.delete("/carts/{cart_id}/", status_code=200)
async def delete_cart(cart_id: UUID, db: Session = Depends(get_db)):
    cart = crud.delete_cart(cart_id, db)
    return cart

@router.get("/carts/", status_code=200)
async def read_carts(db: Session = Depends(get_db)):
    carts = crud.get_carts(db)
    return carts

@router.delete("/carts/", status_code=200)
async def delete_carts(db: Session = Depends(get_db)):
    crud.delete_carts(db)
    return True
