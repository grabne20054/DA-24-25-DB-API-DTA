from fastapi import APIRouter

from crud import crud
from uuid import UUID

router = APIRouter()

@router.post("/ordersProducts/{orderId}/{productId}/{productAmount}/{orderDate}", status_code=201)
async def create_ordersProducts(orderId: UUID, productId: UUID, productAmount: int, orderDate: str = None):
    productId,orderId,productAmount, orderDate = crud.create_ordersProducts(productId, orderId ,productAmount, orderDate)

    response_object = {
        "orderId": orderId,
        "productId": productId,
        "productAmount": productAmount,
        "orderDate": orderDate,
    }
    return response_object

@router.get("/ordersProducts/{orderId}/{productId}", status_code=200)
async def read_ordersProducts(orderId: UUID, productId: UUID):
    ordersProducts = crud.get_ordersProducts(orderId, productId)
    return ordersProducts

@router.delete("/ordersProducts/{orderId}/{productId}", status_code=200)
async def delete_ordersProducts(orderId: UUID, productId: UUID):
    ordersProducts = crud.delete_ordersProducts(orderId, productId)
    return ordersProducts

@router.get("/ordersProducts/", status_code=200)
async def read_ordersProductss():
    ordersProducts = crud.get_ordersProductss()
    return ordersProducts

@router.delete("/ordersProducts/", status_code=200)
async def delete_ordersProductss():
    crud.delete_ordersProductss()
    return True

@router.get("/ordersProductsbyorders/{orderId}", status_code=200)
async def read_ordersProducts_by_orderId(orderId: UUID):
    ordersProducts = crud.get_ordersProducts_by_orderId(orderId)
    return ordersProducts

@router.get("/ordersProductsbyproducts/{productId}", status_code=200)
async def read_ordersProducts_by_productId(productId: UUID):
    ordersProducts = crud.get_ordersProducts_by_productId(productId)
    return ordersProducts
