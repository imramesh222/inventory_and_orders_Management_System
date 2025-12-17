from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .common import TimestampMixin
from pydantic.types import conint

class OrderItemBase(BaseModel):
    item_id: str
    quantity: int

class OrderItemCreate(OrderItemBase):
    item_id: str
    quantity: conint(ge=1)

class OrderItemRead(OrderItemBase, TimestampMixin):
    order_item_id: str
    price: float
    created_at: Optional[datetime] = None  # Make these fields optional
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True