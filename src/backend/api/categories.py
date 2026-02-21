from fastapi import APIRouter, Depends

from crud import crud
from api.model import Category, CategoryDB
from uuid import UUID
from api.check_req_type import allow_get_only
from api.dependencies import get_db
from sqlalchemy.orm import Session

from api.auth import is_token_valid
from typing import Annotated

router = APIRouter(dependencies=[Depends(allow_get_only)])

@router.post("/categories/", response_model=CategoryDB, status_code=201)
async def create_category(token: Annotated[str, Depends(is_token_valid)], payload: Category, db: Session = Depends(get_db)):
    category_id = crud.create_category(payload, db)

    response_object = {
        "categoryId": category_id,
        "name": payload.name,
        "imagePath": payload.imagePath,
        "deleted":payload.deleted
    }
    return response_object


@router.get("/categories/{category_id}/", response_model=CategoryDB, status_code=200)
async def read_category(token: Annotated[str, Depends(is_token_valid)], category_id: UUID, db: Session = Depends(get_db)):
    category = crud.get_category(category_id, db)
    return category

@router.delete("/categories/{category_id}/", status_code=200)
async def delete_category(token: Annotated[str, Depends(is_token_valid)], category_id: UUID, db: Session = Depends(get_db)):
    category = crud.delete_category(category_id, db)
    return category

@router.get("/categories/", status_code=200)
async def read_categories(token: Annotated[str, Depends(is_token_valid)], db: Session = Depends(get_db)):
    categories = crud.get_categories(db)
    return categories

@router.delete("/categories/", status_code=200)
async def delete_categories(token: Annotated[str, Depends(is_token_valid)], db: Session = Depends(get_db)):
    crud.delete_categories(db)
    return True
