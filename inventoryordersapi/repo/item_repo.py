import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select
from model.item_record import ItemRecord
from domain.item import Item
from utils.pagination import paginate_query

class ItemRepo:
    def __init__(self, db: Session):
        self.db = db

    def _record_to_item(self, record: ItemRecord) -> Item:
        """Convert ItemRecord (SQLAlchemy) to Item (Pydantic)"""
        if not record:
            return None
        return Item(
            item_id=str(record.item_id),
            item_name=record.item_name,
            item_description=record.item_description,
            item_price=record.item_price,
            item_quantity=record.item_quantity,
            is_active=record.is_active
        )

    def get(self, item_id: str) -> Item:
        """Get item by ID without locking"""
        record = self.db.query(ItemRecord).filter(ItemRecord.item_id == item_id).first()
        return self._record_to_item(record)
        
    def get_for_update(self, item_id: str) -> ItemRecord:
        """Get item with row lock for update"""
        return self.db.query(ItemRecord).filter(
            ItemRecord.item_id == item_id
        ).with_for_update().first()

    def list_items(self, skip: int = 0, limit: int = 100):
        query = self.db.query(ItemRecord)
        records, pagination = paginate_query(query, limit=limit, offset=skip)
        items = [self._record_to_item(record) for record in records]
        return items, pagination

    def create(self, item: Item) -> Item:
        db_item = ItemRecord(
            item_name=item.item_name,
            item_description=item.item_description,
            item_price=item.item_price,
            item_quantity=item.item_quantity,
            is_active=item.is_active
        )
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return self._record_to_item(db_item)

    def update(self, db_item: ItemRecord, item: Item) -> Item:
        for field, value in item.dict(exclude_unset=True).items():
            if field != 'item_id':  # Don't update the ID
                setattr(db_item, field, value)
        self.db.commit()
        self.db.refresh(db_item)
        return self._record_to_item(db_item)

    def delete(self, db_item: ItemRecord) -> bool:
        self.db.delete(db_item)
        self.db.commit()
        return True
    
    def decrease_item_quantity(self, item_id: str, quantity: int) -> None:
        """
        Decrease item quantity with row lock to prevent race conditions.
        Assumes this is called within an existing transaction.
        """
        item = self.get_for_update(item_id)
        
        if not item:
            raise ValueError(f"Item with ID {item_id} not found")
        
        if item.item_quantity < quantity:
            raise ValueError(
                f"Insufficient stock for item {item.item_name}. "
                f"Available: {item.item_quantity}, Requested: {quantity}"
            )
        
        item.item_quantity -= quantity
        item.updated_at = datetime.datetime.utcnow()
        self.db.add(item)