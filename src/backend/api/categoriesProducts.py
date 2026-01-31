from fastapi import APIRouter

from crud import crud
from uuid import UUID

router = APIRouter()

@router.post("/categoriesProducts/{categoryId}/{productId}", status_code=201)
async def create_categoriesProducts(categoryId: UUID, productId: UUID):
    productId,categoryId = crud.create_categoriesProducts(categoryId, productId)

    response_object = {
        "categoryId": categoryId,
        "productId": productId
    }
    return response_object


@router.get("/categoriesProducts/{categoryId}/{productId}", status_code=200)
async def read_categoriesProducts(categoryId: UUID, productId: UUID):
    categoriesProducts = crud.get_categoriesProducts(categoryId, productId)
    return categoriesProducts

@router.delete("/categoriesProducts/{categoryId}/{productId}", status_code=200)
async def delete_categoriesProducts(categoryId: UUID, productId: UUID):
    categoriesProducts = crud.delete_categoriesProducts(categoryId, productId)
    return categoriesProducts

@router.get("/categoriesProducts/", status_code=200)
async def read_categoriesProductss():
    categoriesProducts = crud.get_categoriesProductss()
    return categoriesProducts

@router.delete("/categoriesProducts/", status_code=200)
async def delete_categoriesProductss():
    crud.delete_categoriesProductss()
    return True

@router.get("/categoriesProductsbycategories/{categoryId}", status_code=200)
async def read_categoriesProducts_by_categoryId(categoryId: UUID):
    categoriesProducts = crud.get_categoriesProducts_by_categoryId(categoryId)
    return categoriesProducts

@router.get("/categoriesProductsbyproducts/{productId}", status_code=200)
async def read_categoriesProducts_by_productId(productId: UUID):
    categoriesProducts = crud.get_categoriesProducts_by_productId(productId)
    return categoriesProducts
