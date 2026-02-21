from fastapi import APIRouter, Depends

from crud import crud
from uuid import UUID
from api.check_req_type import allow_get_only
from api.dependencies import get_db
from sqlalchemy.orm import Session

from api.auth import is_token_valid
from typing import Annotated

router = APIRouter(dependencies=[Depends(allow_get_only)])

@router.post("/cartsProducts/{cartId}/{productId}/{productAmount}", status_code=201)
async def create_cartsProducts(token: Annotated[str, Depends(is_token_valid)], cartId: UUID, productId: UUID, productAmount: int, db: Session = Depends(get_db)):
    productId, cartId, productAmount = crud.create_cartsProducts(cartId, productId, productAmount, db)

    response_object = {
        "cartId": cartId,
        "productId": productId,
        "productAmount": productAmount
    }
    return response_object

@router.get("/cartsProducts/{cartId}/{productId}", status_code=200)
async def read_cartsProducts(token: Annotated[str, Depends(is_token_valid)], cartId: UUID, productId: UUID, db: Session = Depends(get_db)):
    cartsProducts = crud.get_cartsProducts(cartId, productId, db)
    return cartsProducts

@router.delete("/cartsProducts/{cartId}/{productId}", status_code=200)
async def delete_cartsProducts(token: Annotated[str, Depends(is_token_valid)], cartId: UUID, productId: UUID, db: Session = Depends(get_db)):
    cartsProducts = crud.delete_cartsProducts(cartId, productId, db)
    return cartsProducts

@router.get("/cartsProducts/", status_code=200)
async def read_cartsProductss(token: Annotated[str, Depends(is_token_valid)], db: Session = Depends(get_db)):
    cartsProducts = crud.get_cartsProductss(db)
    return cartsProducts

@router.delete("/cartsProducts/", status_code=200)
async def delete_cartsProductss(token: Annotated[str, Depends(is_token_valid)], db: Session = Depends(get_db)):
    crud.delete_cartsProductss(db)
    return True

@router.get("/cartsProductsbycarts/{cartId}", status_code=200)
async def read_cartsProducts_by_cartId(token: Annotated[str, Depends(is_token_valid)], cartId: int, db: Session = Depends(get_db)):
    cartsProducts = crud.get_cartsProducts_by_cartId(cartId, db)
    return cartsProducts

@router.get("/cartsProductsbyproducts/{productId}", status_code=200)
async def read_cartsProducts_by_productId(token: Annotated[str, Depends(is_token_valid)], productId: int, db: Session = Depends(get_db)):
    cartsProducts = crud.get_cartsProducts_by_productId(productId, db)
    return cartsProducts
