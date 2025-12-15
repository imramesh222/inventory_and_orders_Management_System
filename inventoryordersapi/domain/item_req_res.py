from typing import Optional, List

from pydantic import BaseModel
from .item import Item
from .common import BaseResponse, Pagination

class CreateItemRequest(BaseModel):
    item: Item

class CreateItemResponse(BaseResponse):
    item: Optional[Item] = None

class UpdateItemRequest(BaseModel):
    item_id: str
    item: Item

class UpdateItemResponse(BaseResponse):
    item: Optional[Item] = None


class ListItemRequest(BaseModel):
    pagination: Pagination = None

class ListItemResponse(BaseResponse):
    items: List[Item] = []
    pagination: Pagination = None


class GetItemRequest(BaseModel):
    item_id: str

class GetItemResponse(BaseResponse):
    error: bool = False
    msg: Optional[str] = None
    item: Optional[Item] = None