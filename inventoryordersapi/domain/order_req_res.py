from typing import Optional, List

from pydantic import BaseModel
from .order import Order
from .common import BaseResponse, Pagination

class CreateOrderRequest(BaseModel):
    order: Order

class CreateOrderResponse(BaseResponse):
    order: Optional[Order] = None

class UpdateOrderRequest(BaseModel):
    order_id: str
    order: Order

class UpdateOrderResponse(BaseResponse):
    order: Optional[Order] = None


class ListOrderRequest(BaseModel):
    pagination: Pagination = None

class ListOrderResponse(BaseResponse):
    orders: List[Order] = []
    pagination: Pagination = None


class GetOrderRequest(BaseModel):
    order_id: str

class GetOrderResponse(BaseResponse):
    error: bool = False
    msg: Optional[str] = None
    order: Optional[Order] = None