from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from inventoryordersapi.core.security import verify_api_key
from inventoryordersapi.services.order_service import OrderService
from inventoryordersapi.domain.order_req_res import (
    CreateOrderRequest, CreateOrderResponse, 
    GetOrderResponse, UpdateOrderRequest, 
    UpdateOrderResponse, ListOrderResponse
)
from inventoryordersapi.domain.common import ErrorCode
from inventoryordersapi.core.database import get_db
from fastapi import Query

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
    dependencies=[Depends(verify_api_key)]
)

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
    customer_name: str | None = Query(None, description="Filter by customer name"),
    status: str | None = Query(None, description="Filter by order status: paid/unpaid"),
    from_date: str | None = Query(None, description="Filter from date (YYYY-MM-DD)"),
    to_date: str | None = Query(None, description="Filter to date (YYYY-MM-DD)"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Orders per page"),
    db: Session = Depends(get_db)
):
    service = OrderService(db)
    orders, pagination = service.list_orders(
        customer_name=customer_name,
        status=status,
        from_date=from_date,
        to_date=to_date,
        page=page,
        page_size=page_size
    )

    return ListOrderResponse(
        orders=orders,
        pagination=pagination,
        error=False,
        code=200,
        msg="Orders listed successfully"
    )


@router.post("/{order_id}/cancel")
def cancel_order(order_id: str, db: Session = Depends(get_db)):
    service = OrderService(db)
    success = service.cancel_order(order_id)
    if not success:
        raise HTTPException(status_code=400, detail="Cannot cancel order")
    return {"error": False, "code": 200, "msg": "Order canceled successfully"}
