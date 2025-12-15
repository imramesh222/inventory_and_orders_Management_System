from sqlalchemy.orm import Session
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
        record = self.db.query(ItemRecord).filter(ItemRecord.item_id == item_id).first()
        return self._record_to_item(record)

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

    def delete(self, db_item: ItemRecord):
        self.db.delete(db_item)
        self.db.commit()
        return True