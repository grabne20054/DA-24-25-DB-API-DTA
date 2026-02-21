from fastapi import APIRouter, Depends

from crud import crud
from api.model import Product, ProductDB
from uuid import UUID
from api.check_req_type import allow_get_only
from api.dependencies import get_db
from sqlalchemy.orm import Session

from api.auth import is_token_valid
from typing import Annotated

router = APIRouter(dependencies=[Depends(allow_get_only)])

@router.post("/products/", response_model=ProductDB, status_code=201)
async def create_product(token: Annotated[str, Depends(is_token_valid)], payload: Product, db: Session = Depends(get_db)):
    product_id = crud.create_product(payload, db)

    response_object = {
        "productId": product_id,
        "name": payload.name,
        "description": payload.description,
        "price": payload.price,
        "stock": payload.stock,
        "imagePath": payload.imagePath,
        "createdAt":payload.createdAt,
        "deleted":payload.deleted,
        "modifiedAt":payload.modifiedAt,
        }

    return response_object


@router.get("/products/{product_id}/", response_model=ProductDB, status_code=200)
async def read_product(token: Annotated[str, Depends(is_token_valid)], product_id: UUID, db: Session = Depends(get_db)):
    product = crud.get_product(product_id, db)
    return product

@router.delete("/products/{product_id}/", status_code=200)
async def delete_product(token: Annotated[str, Depends(is_token_valid)], product_id: UUID, db: Session = Depends(get_db)):
    product = crud.delete_product(product_id, db)
    return product

@router.get("/products/", status_code=200)
async def read_products(token: Annotated[str, Depends(is_token_valid)], db: Session = Depends(get_db)):
    products = crud.get_products(db)
    return products

@router.delete("/products/", status_code=200)
async def delete_products(token: Annotated[str, Depends(is_token_valid)], db: Session = Depends(get_db)):
    crud.delete_products(db)
    return True
