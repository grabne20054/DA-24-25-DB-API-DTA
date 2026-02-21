from fastapi import APIRouter, Depends

from crud import crud
from api.model import Role, RoleDB
from uuid import UUID
from api.check_req_type import allow_get_only
from api.dependencies import get_db
from sqlalchemy.orm import Session

from api.auth import is_token_valid
from typing import Annotated

router = APIRouter(dependencies=[Depends(allow_get_only)])

@router.post("/roles/", response_model=RoleDB, status_code=201)
async def create_role(token: Annotated[str, Depends(is_token_valid)], payload: Role, db: Session = Depends(get_db)):
    role_id = crud.create_role(payload, db)

    response_object = {
        "roleId": role_id,
        "name": payload.name,
        "description": payload.description,
        "deleted": payload.deleted
    }
    return response_object


@router.get("/roles/{role_id}/", response_model=RoleDB, status_code=200)
async def read_role(token: Annotated[str, Depends(is_token_valid)], role_id: UUID, db: Session = Depends(get_db)):
    role = crud.get_role(role_id, db)
    return role

@router.delete("/roles/{role_id}/", status_code=200)
async def delete_role(token: Annotated[str, Depends(is_token_valid)], role_id: UUID, db: Session = Depends(get_db)):
    role = crud.delete_role(role_id, db)
    return role

@router.get("/roles/", status_code=200)
async def read_roles(token: Annotated[str, Depends(is_token_valid)], db: Session = Depends(get_db)):
    roles = crud.get_roles(db)
    return roles

@router.delete("/roles/", status_code=200)
async def delete_roles(token: Annotated[str, Depends(is_token_valid)], db: Session = Depends(get_db)):
    crud.delete_roles(db)
    return True

@router.get("/roles/name/{name}/", response_model=RoleDB, status_code=200)
async def read_role_by_name(token: Annotated[str, Depends(is_token_valid)], name: str, db: Session = Depends(get_db)):
    role = crud.get_role_by_name(name, db)
    return role