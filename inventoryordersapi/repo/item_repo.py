from sqlalchemy.orm import Session
from model.item_record import ItemRecord
from domain.item import Item
from utils.pagination import paginate_query

class ItemRepo:
    def __init__(self, db: Session):
        self.db = db

    def get(self, item_id: str) -> ItemRecord:
        return self.db.query(ItemRecord).filter(ItemRecord.item_id == item_id).first()

    def list_items(self, skip: int = 0, limit: int = 100):
        query = self.db.query(ItemRecord)
        items, pagination = paginate_query(query, limit=limit, offset=skip)
        return items, pagination

    def create(self, item: Item) -> ItemRecord:
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
        return db_item

    def update(self, db_item: ItemRecord, item: Item) -> ItemRecord:
        for field, value in item.dict(exclude_unset=True).items():
            setattr(db_item, field, value)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def delete(self, db_item: ItemRecord):
        self.db.delete(db_item)
        self.db.commit()
        return True
