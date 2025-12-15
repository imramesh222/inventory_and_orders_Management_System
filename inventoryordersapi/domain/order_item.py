from pydantic import BaseModel
from typing import Optional
from .common import TimestampMixin
from .item import ItemRead

class OrderItemCreate(BaseModel):
    item_id: str
    quantity: int
    price: float

class OrderItemRead(OrderItemCreate, TimestampMixin):
    order_item_id: str
    item: Optional[ItemRead]  # nested item info

    class Config:
        from_attributes = True
