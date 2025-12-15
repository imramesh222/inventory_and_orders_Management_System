from sqlalchemy.orm import Session
from repo.item_repo import ItemRepo
from domain.item import Item
from utils.pagination import paginate_query
from model.item_record import ItemRecord


class ItemService:
    def __init__(self, db: Session):
        self.repo = ItemRepo(db)

    def get_item(self, item_id: str):
        return self.repo.get(item_id)

    def list_items(self, skip: int = 0, limit: int = 100):
        query = self.repo.db.query(ItemRecord)
        items, pagination = paginate_query(query, limit=limit, offset=skip)
        return items, pagination

    def create_item(self, item: Item):
        return self.repo.create(item)

    def update_item(self, item_id: str, item: Item):
        db_item = self.repo.get(item_id)
        if not db_item:
            return None
        return self.repo.update(db_item, item)

    def delete_item(self, item_id: str):
        db_item = self.repo.get(item_id)
        if not db_item:
            return None
        return self.repo.delete(db_item)



