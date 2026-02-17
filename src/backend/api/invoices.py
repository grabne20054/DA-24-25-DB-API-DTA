from fastapi import APIRouter, Depends

from crud import crud
from api.model import Invoice, InvoiceDB
from uuid import UUID
from api.check_req_type import allow_get_only

router = APIRouter(dependencies=[Depends(allow_get_only)])

@router.post("/invoices/", response_model=InvoiceDB, status_code=201)
async def create_invoice(payload: Invoice):
    invoice_id = crud.create_invoice(payload)

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
async def read_invoice(invoice_id: UUID):
    invoice = crud.get_invoice(invoice_id)
    return invoice

@router.delete("/invoices/{invoice_id}/", status_code=200)
async def delete_invoice(invoice_id: UUID):
    invoice = crud.delete_invoice(invoice_id)
    return invoice

@router.get("/invoices/", status_code=200)
async def read_invoices():
    invoices = crud.get_invoices()
    return invoices

@router.delete("/invoices/", status_code=200)
async def delete_invoices():
    crud.delete_invoices()
    return True
