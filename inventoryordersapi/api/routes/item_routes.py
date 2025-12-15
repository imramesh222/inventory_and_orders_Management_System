from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.item_service import ItemService
from domain.item_req_res import CreateItemRequest, CreateItemResponse, GetItemRequest, GetItemResponse, ListItemRequest, ListItemResponse, UpdateItemRequest, UpdateItemResponse
from domain.common import ErrorCode
from core.database import get_db

router = APIRouter()

@router.post("/add_item", response_model=CreateItemResponse)
def create_item(req: CreateItemRequest, db: Session = Depends(get_db)):
    service = ItemService(db)
    item = service.create_item(req.item)
    return CreateItemResponse(item=item, error=False, code=ErrorCode.SUCCESS, msg="Item created successfully")

@router.get("/{item_id}", response_model=GetItemResponse)
def get_item(item_id: str, db: Session = Depends(get_db)):
    service = ItemService(db)
    item = service.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return GetItemResponse(item=item, error=False, code=ErrorCode.SUCCESS, msg="Item fetched successfully")

@router.put("/{item_id}", response_model=UpdateItemResponse)
def update_item(item_id: str, req: UpdateItemRequest, db: Session = Depends(get_db)):
    service = ItemService(db)
    updated_item = service.update_item(item_id, req.item)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return UpdateItemResponse(item=updated_item, error=False, code=ErrorCode.SUCCESS, msg="Item updated successfully")

@router.get("/", response_model=ListItemResponse)
def list_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = ItemService(db)
    items = service.list_items(skip=skip, limit=limit)
    return ListItemResponse(items=items, error=False, code=ErrorCode.SUCCESS, msg="Items listed successfully")