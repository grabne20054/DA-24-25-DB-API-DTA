from fastapi import APIRouter, Depends

from crud import crud
from uuid import UUID
from api.check_req_type import allow_get_only
from api.dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter(dependencies=[Depends(allow_get_only)])

@router.post("/categoriesProducts/{categoryId}/{productId}", status_code=201)
async def create_categoriesProducts(categoryId: UUID, productId: UUID, db: Session = Depends(get_db)):
    productId,categoryId = crud.create_categoriesProducts(categoryId, productId, db)

    response_object = {
        "categoryId": categoryId,
        "productId": productId
    }
    return response_object


@router.get("/categoriesProducts/{categoryId}/{productId}", status_code=200)
async def read_categoriesProducts(categoryId: UUID, productId: UUID, db: Session = Depends(get_db)):
    categoriesProducts = crud.get_categoriesProducts(categoryId, productId, db)
    return categoriesProducts

@router.delete("/categoriesProducts/{categoryId}/{productId}", status_code=200)
async def delete_categoriesProducts(categoryId: UUID, productId: UUID, db: Session = Depends(get_db)):
    categoriesProducts = crud.delete_categoriesProducts(categoryId, productId, db)
    return categoriesProducts

@router.get("/categoriesProducts/", status_code=200)
async def read_categoriesProductss(db: Session = Depends(get_db)):
    categoriesProducts = crud.get_categoriesProductss(db)
    return categoriesProducts

@router.delete("/categoriesProducts/", status_code=200)
async def delete_categoriesProductss(db: Session = Depends(get_db)):
    crud.delete_categoriesProductss(db)
    return True

@router.get("/categoriesProductsbycategories/{categoryId}", status_code=200)
async def read_categoriesProducts_by_categoryId(categoryId: UUID, db: Session = Depends(get_db)):
    categoriesProducts = crud.get_categoriesProducts_by_categoryId(categoryId, db)
    return categoriesProducts

@router.get("/categoriesProductsbyproducts/{productId}", status_code=200)
async def read_categoriesProducts_by_productId(productId: UUID, db: Session = Depends(get_db)):
    categoriesProducts = crud.get_categoriesProducts_by_productId(productId, db)
    return categoriesProducts
