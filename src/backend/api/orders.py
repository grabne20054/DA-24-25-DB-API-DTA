from fastapi import APIRouter, Depends

from crud import crud
from api.model import Order, OrderDB
from uuid import UUID
from api.check_req_type import allow_get_only

router = APIRouter(dependencies=[Depends(allow_get_only)])

@router.post("/orders/", response_model=OrderDB, status_code=201)
async def create_orders(payload: Order):
    order_id = crud.create_order(payload)

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
async def read_order(order_id: UUID):
    order = crud.get_order(order_id)
    return order

@router.delete("/orders/{order_id}/", status_code=200)
async def delete_order(order_id: UUID):
    order = crud.delete_order(order_id)
    return order

@router.get("/orders/", status_code=200)
async def read_orders():
    orders = crud.get_orders()
    return orders

@router.delete("/orders/", status_code=200)
async def delete_orders():
    crud.delete_orders()
    return True
