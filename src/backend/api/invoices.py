from fastapi import APIRouter, Depends

from crud import crud
from api.model import Invoice, InvoiceDB
from uuid import UUID
from api.check_req_type import allow_get_only
from api.dependencies import get_db
from sqlalchemy.orm import Session

from api.auth import is_token_valid
from typing import Annotated

router = APIRouter(dependencies=[Depends(allow_get_only)])

@router.post("/invoices/", response_model=InvoiceDB, status_code=201)
async def create_invoice(token: Annotated[str, Depends(is_token_valid)], payload: Invoice, db: Session = Depends(get_db)):
    invoice_id = crud.create_invoice(payload, db)

    response_object = {
        "invoiceId": invoice_id,
        "orderId": payload.orderId,
        "invoiceAmount": payload.invoiceAmount,
        "paymentDate": payload.paymentDate,
        "pdfUrl":payload.pdfUrl,
        "deleted":payload.deleted,
    }
    return response_object


@router.get("/invoices/{invoice_id}/", response_model=InvoiceDB, status_code=200)
async def read_invoice(token: Annotated[str, Depends(is_token_valid)], invoice_id: UUID, db: Session = Depends(get_db)):
    invoice = crud.get_invoice(invoice_id, db)
    return invoice

@router.delete("/invoices/{invoice_id}/", status_code=200)
async def delete_invoice(token: Annotated[str, Depends(is_token_valid)], invoice_id: UUID, db: Session = Depends(get_db)):
    invoice = crud.delete_invoice(invoice_id, db)
    return invoice

@router.get("/invoices/", status_code=200)
async def read_invoices(token: Annotated[str, Depends(is_token_valid)], db: Session = Depends(get_db)):
    invoices = crud.get_invoices(db)
    return invoices

@router.delete("/invoices/", status_code=200)
async def delete_invoices(token: Annotated[str, Depends(is_token_valid)], db: Session = Depends(get_db)):
    crud.delete_invoices(db)
    return True
