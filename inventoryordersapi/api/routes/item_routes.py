from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from inventoryordersapi.services.item_service import ItemService
from inventoryordersapi.domain.item_req_res import (
    CreateItemRequest,
    CreateItemResponse,
    GetItemResponse,
    ListItemResponse,
    UpdateItemRequest,
    UpdateItemResponse
)
from inventoryordersapi.domain.common import ErrorCode
from inventoryordersapi.core.database import get_db
from inventoryordersapi.core.security import verify_api_key

# 🔐 API key applied to ALL routes in this router
router = APIRouter(
    prefix="/items",
    tags=["Items"],
    dependencies=[Depends(verify_api_key)]
)

@router.post("/add_item", response_model=CreateItemResponse)
def create_item(req: CreateItemRequest, db: Session = Depends(get_db)):
    service = ItemService(db)
    item = service.create_item(req.item)

    return CreateItemResponse(
        item=item,
        error=False,
        code=ErrorCode.SUCCESS,
        msg="Item created successfully"
    )

@router.get("/{item_id}", response_model=GetItemResponse)
def get_item(item_id: str, db: Session = Depends(get_db)):
    service = ItemService(db)
    item = service.get_item(item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return GetItemResponse(
        item=item,
        error=False,
        code=ErrorCode.SUCCESS,
        msg="Item fetched successfully"
    )

@router.put("/{item_id}", response_model=UpdateItemResponse)
def update_item(item_id: str, req: UpdateItemRequest, db: Session = Depends(get_db)):
    service = ItemService(db)
    updated_item = service.update_item(item_id, req.item)

    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")

    return UpdateItemResponse(
        item=updated_item,
        error=False,
        code=ErrorCode.SUCCESS,
        msg="Item updated successfully"
    )

@router.get("/", response_model=ListItemResponse)
def list_items(
    search: str | None = Query(None, description="Search term for item name/description"),
    min_price: float | None = Query(None, description="Minimum price"),
    max_price: float | None = Query(None, description="Maximum price"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    service = ItemService(db)
    items, pagination = service.list_items(
        search=search,
        min_price=min_price,
        max_price=max_price,
        page=page,
        page_size=page_size
    )

    return ListItemResponse(
        items=items,
        pagination=pagination,
        error=False,
        code=ErrorCode.SUCCESS,
        msg="Items listed successfully"
    )

@router.delete("/{item_id}", response_model=UpdateItemResponse)
def delete_item(item_id: str, db: Session = Depends(get_db)):
    service = ItemService(db)
    deleted_item = service.delete_item(item_id)

    if not deleted_item:
        raise HTTPException(status_code=404, detail="Item not found or already deleted")

    return UpdateItemResponse(
        item=deleted_item,
        error=False,
        code=ErrorCode.SUCCESS,
        msg="Item soft-deleted successfully"
    )
