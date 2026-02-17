from fastapi import APIRouter, Depends

from crud import crud
from api.model import Role, RoleDB
from uuid import UUID
from api.check_req_type import allow_get_only

router = APIRouter(dependencies=[Depends(allow_get_only)])

@router.post("/roles/", response_model=RoleDB, status_code=201)
async def create_role(payload: Role):
    role_id = crud.create_role(payload)

    response_object = {
        "roleId": role_id,
        "name": payload.name,
        "description": payload.description,
        "deleted": payload.deleted
    }
    return response_object


@router.get("/roles/{role_id}/", response_model=RoleDB, status_code=200)
async def read_role(role_id: UUID):
    role = crud.get_role(role_id)
    return role

@router.delete("/roles/{role_id}/", status_code=200)
async def delete_role(role_id: UUID):
    role = crud.delete_role(role_id)
    return role

@router.get("/roles/", status_code=200)
async def read_roles():
    roles = crud.get_roles()
    return roles

@router.delete("/roles/", status_code=200)
async def delete_roles():
    crud.delete_roles()
    return True

@router.get("/roles/name/{name}/", response_model=RoleDB, status_code=200)
async def read_role_by_name(name: str):
    role = crud.get_role_by_name(name)
    return role