from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .common import TimestampMixin

class OrderItemBase(BaseModel):
    item_id: str
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemRead(OrderItemBase, TimestampMixin):
    order_item_id: str
    price: float
    created_at: Optional[datetime] = None  # Make these fields optional
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True