
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .common import TimestampMixin

# For creating a new item
class Item(BaseModel):
    item_id: Optional[str] = None
    item_name: str
    item_description: Optional[str] = None
    item_price: float
    item_quantity: int
    is_active: Optional[bool] = True
    low_stock: bool

# For reading an item (includes ID and timestamps)
class ItemRead(Item, TimestampMixin):
    item_id: Optional[str] = None
    low_stock: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
