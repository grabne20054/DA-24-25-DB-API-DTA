from fastapi import APIRouter, Depends

from crud import crud
from uuid import UUID
from api.check_req_type import allow_get_only
from api.dependencies import get_db
from sqlalchemy.orm import Session

from api.auth import is_token_valid
from typing import Annotated

router = APIRouter(dependencies=[Depends(allow_get_only)])

@router.post("/ordersProducts/{orderId}/{productId}/{productAmount}/{orderDate}", status_code=201)
async def create_ordersProducts(token: Annotated[str, Depends(is_token_valid)], orderId: UUID, productId: UUID, productAmount: int, orderDate: str = None, db: Session = Depends(get_db)):
    productId,orderId,productAmount, orderDate = crud.create_ordersProducts(productId, orderId ,productAmount, orderDate, db)

    response_object = {
        "orderId": orderId,
        "productId": productId,
        "productAmount": productAmount,
        "orderDate": orderDate,
    }
    return response_object

@router.get("/ordersProducts/{orderId}/{productId}", status_code=200)
async def read_ordersProducts(token: Annotated[str, Depends(is_token_valid)], orderId: UUID, productId: UUID, db: Session = Depends(get_db)):
    ordersProducts = crud.get_ordersProducts(orderId, productId, db)
    return ordersProducts

@router.delete("/ordersProducts/{orderId}/{productId}", status_code=200)
async def delete_ordersProducts(token: Annotated[str, Depends(is_token_valid)], orderId: UUID, productId: UUID, db: Session = Depends(get_db)):
    ordersProducts = crud.delete_ordersProducts(orderId, productId, db)
    return ordersProducts

@router.get("/ordersProducts/", status_code=200)
async def read_ordersProductss(token: Annotated[str, Depends(is_token_valid)], db: Session = Depends(get_db)):
    ordersProducts = crud.get_ordersProductss(db)
    return ordersProducts

@router.delete("/ordersProducts/", status_code=200)
async def delete_ordersProductss(token: Annotated[str, Depends(is_token_valid)], db: Session = Depends(get_db)):
    crud.delete_ordersProductss(db)
    return True

@router.get("/ordersProductsbyorders/{orderId}", status_code=200)
async def read_ordersProducts_by_orderId(token: Annotated[str, Depends(is_token_valid)], orderId: UUID, db: Session = Depends(get_db)):
    ordersProducts = crud.get_ordersProducts_by_orderId(orderId, db)
    return ordersProducts

@router.get("/ordersProductsbyproducts/{productId}", status_code=200)
async def read_ordersProducts_by_productId(token: Annotated[str, Depends(is_token_valid)], productId: UUID, db: Session = Depends(get_db)):
    ordersProducts = crud.get_ordersProducts_by_productId(productId, db)
    return ordersProducts
