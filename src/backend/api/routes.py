from fastapi import APIRouter, Depends

from crud import crud
from api.model import Route, RouteDB
from uuid import UUID
from api.check_req_type import allow_get_only
from api.dependencies import get_db
from sqlalchemy.orm import Session

from api.auth import is_token_valid
from typing import Annotated

router = APIRouter(dependencies=[Depends(allow_get_only)])

@router.post("/routes/", response_model=RouteDB, status_code=201)
async def create_route(token: Annotated[str, Depends(is_token_valid)], payload: Route, db: Session = Depends(get_db)):
    route_id = crud.create_route(payload, db)

    response_object = {
        "routeId": route_id,
        "name": payload.name,
        "deleted": payload.deleted,
    }
    return response_object


@router.get("/routes/{route_id}/", response_model=RouteDB, status_code=200)
async def read_route(token: Annotated[str, Depends(is_token_valid)], route_id: UUID, db: Session = Depends(get_db)):
    route = crud.get_route(route_id, db)
    return route

@router.delete("/routes/{route_id}/", status_code=200)
async def delete_route(token: Annotated[str, Depends(is_token_valid)], route_id: UUID, db: Session = Depends(get_db)):
    route = crud.delete_route(route_id, db)
    return route

@router.get("/routes/", status_code=200)
async def read_routes(token: Annotated[str, Depends(is_token_valid)], db: Session = Depends(get_db)):
    routes = crud.get_routes(db)
    return routes

@router.delete("/routes/", status_code=200)
async def delete_routes(token: Annotated[str, Depends(is_token_valid)], db: Session = Depends(get_db)):
    crud.delete_routes(db)
    return True
