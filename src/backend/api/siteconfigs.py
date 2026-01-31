from fastapi import APIRouter

from api.model import SiteConfig, SiteConfigDB
from crud import crud
from uuid import UUID


router = APIRouter()

@router.post("/siteconfigs/", response_model=SiteConfigDB, status_code=201)
async def create_siteconfig(payload: SiteConfig):
    siteconfig_id = await crud.create_site_config(payload)

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
async def read_siteconfig(siteconfig_id: UUID):
    siteconfig = await crud.get_site_config(siteconfig_id)
    return siteconfig

@router.delete("/siteconfigs/{siteconfig_id}/", response_model=SiteConfigDB, status_code=200)
async def delete_siteconfig(siteconfig_id: UUID):
    siteconfig = await crud.delete_siteconfig(siteconfig_id)
    return siteconfig

@router.get("/siteconfigs/", status_code=200)
async def read_siteconfigs():
    siteconfig =  crud.get_site_configs()
    return siteconfig

@router.delete("/siteconfigs/", status_code=200)
async def delete_siteconfigs():
    siteconfig = await crud.delete_siteconfigs()
    return siteconfig