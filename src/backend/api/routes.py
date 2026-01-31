from fastapi import APIRouter

from crud import crud
from api.model import Route, RouteDB
from uuid import UUID

router = APIRouter()

@router.post("/routes/", response_model=RouteDB, status_code=201)
async def create_route(payload: Route):
    route_id = crud.create_route(payload)

    response_object = {
        "routeId": route_id,
        "name": payload.name,
        "deleted": payload.deleted,
    }
    return response_object


@router.get("/routes/{route_id}/", response_model=RouteDB, status_code=200)
async def read_route(route_id: UUID):
    route = crud.get_route(route_id)
    return route

@router.delete("/routes/{route_id}/", status_code=200)
async def delete_route(route_id: UUID):
    route = crud.delete_route(route_id)
    return route

@router.get("/routes/", status_code=200)
async def read_routes():
    routes = crud.get_routes()
    return routes

@router.delete("/routes/", status_code=200)
async def delete_routes():
    crud.delete_routes()
    return True
