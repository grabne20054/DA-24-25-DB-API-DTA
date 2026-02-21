from fastapi import APIRouter, Depends

from api.model import SiteConfig, SiteConfigDB
from crud import crud
from uuid import UUID
from api.check_req_type import allow_get_only
from api.dependencies import get_db
from sqlalchemy.orm import Session

from api.auth import is_token_valid
from typing import Annotated

router = APIRouter(dependencies=[Depends(allow_get_only)])

@router.post("/siteconfigs/", response_model=SiteConfigDB, status_code=201)
async def create_siteconfig(token: Annotated[str, Depends(is_token_valid)], payload: SiteConfig, db: Session = Depends(get_db)):
    siteconfig_id = await crud.create_site_config(payload, db)

    response_object = {
        "id": siteconfig_id,
        "companyName": payload.companyName,
        "logoPath": payload.logoPath,
        "email": payload.email,
        "phoneNumber": payload.phoneNumber,
        "companyNumber": payload.companyNumber,
        "iban": payload.iban,
        "addressId": payload.addressId

    }
    return response_object

@router.get("/siteconfigs/{siteconfig_id}/", response_model=SiteConfigDB, status_code=200)
async def read_siteconfig(token: Annotated[str, Depends(is_token_valid)], siteconfig_id: UUID, db: Session = Depends(get_db)):
    siteconfig = await crud.get_site_config(siteconfig_id, db)
    return siteconfig

@router.delete("/siteconfigs/{siteconfig_id}/", response_model=SiteConfigDB, status_code=200)
async def delete_siteconfig(token: Annotated[str, Depends(is_token_valid)], siteconfig_id: UUID, db: Session = Depends(get_db)):
    siteconfig = await crud.delete_siteconfig(siteconfig_id, db)
    return siteconfig

@router.get("/siteconfigs/", status_code=200)
async def read_siteconfigs(token: Annotated[str, Depends(is_token_valid)], db: Session = Depends(get_db)):
    siteconfig =  crud.get_site_configs(db)
    return siteconfig

@router.delete("/siteconfigs/", status_code=200)
async def delete_siteconfigs(token: Annotated[str, Depends(is_token_valid)], db: Session = Depends(get_db)):
    siteconfig = await crud.delete_siteconfigs(db)
    return siteconfig