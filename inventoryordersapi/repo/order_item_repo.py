from sqlalchemy.orm import Session
from model.order_item_record import OrderItemRecord

class OrderItemRepo:
    def __init__(self, db: Session):
        self.db = db

    def create(self, order_item: OrderItemRecord) -> OrderItemRecord:
        self.db.add(order_item)
        self.db.commit()
        self.db.refresh(order_item)
        return order_item

    def delete(self, db_order_item: OrderItemRecord):
        self.db.delete(db_order_item)
        self.db.commit()
        return True
