from fastapi import APIRouter, Depends

from crud import crud
from uuid import UUID
from api.check_req_type import allow_get_only

router = APIRouter(dependencies=[Depends(allow_get_only)])

@router.post("/routesOrders/{routeId}/{orderId}", status_code=201)
async def create_routesOrders(routeId: UUID, orderId: UUID):
    routeId,orderId = crud.create_routesOrders(routeId, orderId)

    response_object = {
        "routeId": routeId,
        "orderId": orderId
    }
    return response_object

@router.get("/routesOrders/{routeId}/{orderId}", status_code=200)
async def read_routesOrders(routeId: UUID, orderId: UUID):
    routesOrders = crud.get_routesOrders(routeId, orderId)
    return routesOrders

@router.delete("/routesOrders/{routeId}/{orderId}", status_code=200)
async def delete_routesOrders(routeId: UUID, orderId: UUID):
    routesOrders = crud.delete_routesOrders(routeId, orderId)
    return routesOrders

@router.get("/routesOrders/", status_code=200)
async def read_routesOrderss():
    routesOrders = crud.get_routesOrderss()
    return routesOrders

@router.delete("/routesOrders/", status_code=200)
async def delete_routesOrderss():
    crud.delete_routesOrderss()
    return True

@router.get("/routesOrdersbyroutes/{routeId}", status_code=200)
async def read_routesOrders_by_routeId(routeId: UUID):
    routesOrders = crud.get_routesOrders_by_routeId(routeId)
    return routesOrders

@router.get("/routesOrdersbyorders/{orderId}", status_code=200)
async def read_routesOrders_by_orderId(orderId: UUID):
    routesOrders = crud.get_routesOrders_by_orderId(orderId)
    return routesOrders
