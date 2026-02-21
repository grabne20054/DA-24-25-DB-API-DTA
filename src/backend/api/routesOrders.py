from fastapi import APIRouter, Depends

from crud import crud
from uuid import UUID
from api.check_req_type import allow_get_only
from api.dependencies import get_db
from sqlalchemy.orm import Session

from api.auth import is_token_valid
from typing import Annotated

router = APIRouter(dependencies=[Depends(allow_get_only)])

@router.post("/routesOrders/{routeId}/{orderId}", status_code=201)
async def create_routesOrders(token: Annotated[str, Depends(is_token_valid)], routeId: UUID, orderId: UUID, db: Session = Depends(get_db)):
    routeId, orderId = crud.create_routesOrders(routeId, orderId, db)

    response_object = {
        "routeId": routeId,
        "orderId": orderId
    }
    return response_object

@router.get("/routesOrders/{routeId}/{orderId}", status_code=200)
async def read_routesOrders(token: Annotated[str, Depends(is_token_valid)], routeId: UUID, orderId: UUID, db: Session = Depends(get_db)):
    routesOrders = crud.get_routesOrders(routeId, orderId, db)
    return routesOrders

@router.delete("/routesOrders/{routeId}/{orderId}", status_code=200)
async def delete_routesOrders(token: Annotated[str, Depends(is_token_valid)], routeId: UUID, orderId: UUID, db: Session = Depends(get_db)):
    routesOrders = crud.delete_routesOrders(routeId, orderId, db)
    return routesOrders

@router.get("/routesOrders/", status_code=200)
async def read_routesOrderss(token: Annotated[str, Depends(is_token_valid)], db: Session = Depends(get_db)):
    routesOrders = crud.get_routesOrderss(db)
    return routesOrders

@router.delete("/routesOrders/", status_code=200)
async def delete_routesOrderss(token: Annotated[str, Depends(is_token_valid)], db: Session = Depends(get_db)):
    crud.delete_routesOrderss(db)
    return True

@router.get("/routesOrdersbyroutes/{routeId}", status_code=200)
async def read_routesOrders_by_routeId(token: Annotated[str, Depends(is_token_valid)], routeId: UUID, db: Session = Depends(get_db)):
    routesOrders = crud.get_routesOrders_by_routeId(routeId, db)
    return routesOrders

@router.get("/routesOrdersbyorders/{orderId}", status_code=200)
async def read_routesOrders_by_orderId(token: Annotated[str, Depends(is_token_valid)], orderId: UUID, db: Session = Depends(get_db)):
    routesOrders = crud.get_routesOrders_by_orderId(orderId, db)
    return routesOrders
