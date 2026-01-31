from fastapi import APIRouter

from crud import crud
from api.model import Product, ProductDB
from uuid import UUID

router = APIRouter()

@router.post("/products/", response_model=ProductDB, status_code=201)
async def create_product(payload: Product):
    product_id = crud.create_product(payload)

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
async def read_product(product_id: UUID):
    product = crud.get_product(product_id)
    return product

@router.delete("/products/{product_id}/", status_code=200)
async def delete_product(product_id: UUID):
    product = crud.delete_product(product_id)
    return product

@router.get("/products/", status_code=200)
async def read_products():
    products = crud.get_products()
    return products

@router.delete("/products/", status_code=200)
async def delete_products():
    crud.delete_products()
    return True
