from fastapi import APIRouter, Depends

from crud import crud
from api.model import Order, OrderDB
from uuid import UUID
from api.check_req_type import allow_get_only
from api.dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter(dependencies=[Depends(allow_get_only)])

@router.post("/orders/", response_model=OrderDB, status_code=201)
async def create_orders(payload: Order, db: Session = Depends(get_db)):
    order_id = crud.create_order(payload, db)

    response_object = {
        "orderId": order_id,
        "orderDate": payload.orderDate,
        "deliveryDate": payload.deliveryDate,
        "customerReference": payload.customerReference,
        "orderState": payload.orderState,
        "selfCollect": payload.selfCollect,
        "deleted": payload.deleted
    }
    return response_object


@router.get("/orders/{order_id}/", response_model=OrderDB, status_code=200)
async def read_order(order_id: UUID, db: Session = Depends(get_db)):
    order = crud.get_order(order_id, db)
    return order

@router.delete("/orders/{order_id}/", status_code=200)
async def delete_order(order_id: UUID, db: Session = Depends(get_db)):
    order = crud.delete_order(order_id, db)
    return order

@router.get("/orders/", status_code=200)
async def read_orders(db: Session = Depends(get_db)):
    orders = crud.get_orders(db)
    return orders

@router.delete("/orders/", status_code=200)
async def delete_orders(db: Session = Depends(get_db)):
    crud.delete_orders(db)
    return True
