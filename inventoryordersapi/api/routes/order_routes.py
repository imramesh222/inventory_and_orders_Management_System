from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.order_service import OrderService
from domain.order_req_res import (
    CreateOrderRequest, CreateOrderResponse, 
    GetOrderResponse, UpdateOrderRequest, 
    UpdateOrderResponse, ListOrderResponse
)
from domain.common import ErrorCode
from core.database import get_db

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=CreateOrderResponse)
def create_order(request: CreateOrderRequest, db: Session = Depends(get_db)):
    service = OrderService(db)
    response = service.create_order(request)
    
    if response.error:
        status_code = 400 if response.code == ErrorCode.BAD_REQUEST else 500
        raise HTTPException(
            status_code=status_code,
            detail=response.msg
        )
    
    return response

@router.get("/{order_id}", response_model=GetOrderResponse)
def get_order(order_id: str, db: Session = Depends(get_db)):
    service = OrderService(db)
    response = service.get_order(order_id)
    
    if response.error:
        status_code = 404 if response.code == ErrorCode.NOT_FOUND else 500
        raise HTTPException(
            status_code=status_code,
            detail=response.msg
        )
    
    return response

@router.put("/{order_id}", response_model=UpdateOrderResponse)
def update_order(
    order_id: str, 
    request: UpdateOrderRequest, 
    db: Session = Depends(get_db)
):
    service = OrderService(db)
    response = service.update_order(order_id, request)
    
    if response.error:
        status_code = 404 if response.code == ErrorCode.NOT_FOUND else 500
        raise HTTPException(
            status_code=status_code,
            detail=response.msg
        )
    
    return response

@router.get("/", response_model=ListOrderResponse)
def list_orders(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    service = OrderService(db)
    response = service.list_orders(skip=skip, limit=limit)
    
    if response.error:
        raise HTTPException(
            status_code=500,
            detail=response.msg
        )
    
    return response