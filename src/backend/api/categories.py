from fastapi import APIRouter, Depends

from crud import crud
from api.model import Category, CategoryDB
from uuid import UUID
from api.check_req_type import allow_get_only

router = APIRouter(dependencies=[Depends(allow_get_only)])

@router.post("/categories/", response_model=CategoryDB, status_code=201)
async def create_category(payload: Category):
    category_id = crud.create_category(payload)

    response_object = {
        "categoryId": category_id,
        "name": payload.name,
        "imagePath": payload.imagePath,
        "deleted":payload.deleted
    }
    return response_object


@router.get("/categories/{category_id}/", response_model=CategoryDB, status_code=200)
async def read_category(category_id: UUID):
    category = crud.get_category(category_id)
    return category

@router.delete("/categories/{category_id}/", status_code=200)
async def delete_category(category_id: UUID):
    category = crud.delete_category(category_id)
    return category

@router.get("/categories/", status_code=200)
async def read_categories():
    categories = crud.get_categories()
    return categories

@router.delete("/categories/", status_code=200)
async def delete_categories():
    crud.delete_categories()
    return True
