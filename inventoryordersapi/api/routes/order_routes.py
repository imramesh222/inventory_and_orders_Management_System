from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.order_service import OrderService
from domain.order_req_res import CreateOrderRequest, CreateOrderResponse, GetOrderRequest, GetOrderResponse, UpdateOrderRequest, UpdateOrderResponse, ListOrderResponse
from core.database import get_db

router = APIRouter()

@router.post("/", response_model=CreateOrderResponse)
def create_order(req: CreateOrderRequest, db: Session = Depends(get_db)):
    service = OrderService(db)
    try:
        order = service.create_order(req.order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return CreateOrderResponse(order=order, error=False, code=200, msg="Order created successfully")

@router.get("/{order_id}", response_model=GetOrderResponse)
def get_order(order_id: str, db: Session = Depends(get_db)):
    service = OrderService(db)
    order = service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return GetOrderResponse(order=order, error=False, code=200, msg="Order fetched successfully")

@router.put("/{order_id}", response_model=UpdateOrderResponse)
def update_order(order_id: str, req: UpdateOrderRequest, db: Session = Depends(get_db)):
    service = OrderService(db)
    updated_order = service.update_order(order_id, req.order.dict(exclude_unset=True))
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return UpdateOrderResponse(order=updated_order, error=False, code=200, msg="Order updated successfully")

@router.get("/", response_model=ListOrderResponse)
def list_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = OrderService(db)
    orders = service.list_orders(skip=skip, limit=limit)
    return ListOrderResponse(orders=orders, error=False, code=200, msg="Orders listed successfully")
