from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from inventoryordersapi.repo.item_repo import ItemRepo
from inventoryordersapi.domain.item import Item
from inventoryordersapi.utils.pagination import paginate_query
from inventoryordersapi.model.item_record import ItemRecord

class ItemService:
    def __init__(self, db: Session):
        self.repo = ItemRepo(db)

    def get_item(self, item_id: str):
        return self.repo.get(item_id)

    def list_items(
        self,
        search: str | None,
        min_price: float | None,
        max_price: float | None,
        page: int,
        page_size: int
    ):
        query = self.repo.db.query(ItemRecord).filter(
            ItemRecord.is_active == True
        )

        #  Search filter
        if search:
            query = query.filter(
                or_(
                    ItemRecord.item_name.ilike(f"%{search}%"),
                    ItemRecord.item_description.ilike(f"%{search}%")
                )
            )

        #  Price filters
        if min_price is not None:
            query = query.filter(ItemRecord.item_price >= min_price)

        if max_price is not None:
            query = query.filter(ItemRecord.item_price <= max_price)

        #  Pagination
        offset = (page - 1) * page_size
        records, pagination = paginate_query(
            query,
            limit=page_size,
            offset=offset,
            page=page,
            page_size=page_size
        )

        #  Map + low_stock
        items = [
            {
                **record.__dict__,
                "low_stock": record.item_quantity < 5
            }
            for record in records
        ]

        return items, pagination

    def create_item(self, item: Item):
        # Check if an active item with the same name already exists
        if self.repo.exists_active_name(item.item_name):
            raise HTTPException(
                status_code=400,
                detail="An active item with this name already exists"
            )

        return self.repo.create(item)
    
    def update_item(self, item_id: str, item: Item):
        # Fetch active item record
        db_item = self.repo.db.query(ItemRecord).filter(
            ItemRecord.item_id == item_id,
            ItemRecord.is_active == True
        ).first()

        if not db_item:
            return None

        #  Enforce name uniqueness among active items
        if item.item_name:
            if self.repo.exists_active_name(
                item.item_name,
                exclude_id=item_id
            ):
                raise HTTPException(
                    status_code=400,
                    detail="Another active item with this name already exists"
                )

        return self.repo.update(db_item, item)

    

    def delete_item(self, item_id: str):
        db_item = self.repo.get_for_update(item_id)
        if not db_item or not db_item.is_active:
            return None
        return self.repo.soft_delete(db_item)



