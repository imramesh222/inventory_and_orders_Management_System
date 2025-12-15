from pydantic import BaseModel
from typing import List
from .common import TimestampMixin
from .order_item import OrderItemRead, OrderItemCreate

class Order(BaseModel):
    customer_name: str
    customer_email: str
    order_items: List[OrderItemCreate]  # list of order items

class OrderRead(Order, TimestampMixin):
    order_id: str
    total_amount: float
    is_paid: bool
    order_items: List[OrderItemRead]  # nested order items with details

    class Config:
        from_attributes = True
