from fastapi import APIRouter, Depends

from crud import crud
from uuid import UUID
from api.check_req_type import allow_get_only

router = APIRouter(dependencies=[Depends(allow_get_only)])

@router.post("/cartsProducts/{cartId}/{productId}/{productAmount}", status_code=201)
async def create_cartsProducts(cartId: UUID, productId: UUID, productAmount: int):	
    productId,cartId,productAmount  = crud.create_cartsProducts(cartId, productId, productAmount)

    response_object = {
        "cartId": cartId,
        "productId": productId,
        "productAmount": productAmount
    }
    return response_object

@router.get("/cartsProducts/{cartId}/{productId}", status_code=200)
async def read_cartsProducts(cartId: UUID, productId: UUID):
    cartsProducts = crud.get_cartsProducts(cartId, productId)
    return cartsProducts

@router.delete("/cartsProducts/{cartId}/{productId}", status_code=200)
async def delete_cartsProducts(cartId: UUID, productId: UUID):
    cartsProducts = crud.delete_cartsProducts(cartId, productId)
    return cartsProducts

@router.get("/cartsProducts/", status_code=200)
async def read_cartsProductss():
    cartsProducts = crud.get_cartsProductss()
    return cartsProducts

@router.delete("/cartsProducts/", status_code=200)
async def delete_cartsProductss():
    crud.delete_cartsProductss()
    return True

@router.get("/cartsProductsbycarts/{cartId}", status_code=200)
async def read_cartsProducts_by_cartId(cartId: int):
    cartsProducts = crud.get_cartsProducts_by_cartId(cartId)
    return cartsProducts

@router.get("/cartsProductsbyproducts/{productId}", status_code=200)
async def read_cartsProducts_by_productId(productId: int):
    cartsProducts = crud.get_cartsProducts_by_productId(productId)
    return cartsProducts
