from pydantic import BaseModel
from typing import List

class OrderItemResponse(BaseModel):
    item_id: str
    name: str
    unit_price: float
    quantity: int
    line_total: float

class OrderResponse(BaseModel):
    id: str
    customer_name: str
    status: str
    total_amount: float
    created_at: str
    items: List[OrderItemResponse]
