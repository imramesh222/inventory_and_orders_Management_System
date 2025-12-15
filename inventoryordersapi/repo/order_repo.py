from sqlalchemy.orm import Session
from model.order_record import OrderRecord
from domain.order_req_res import CreateOrderRequest
from utils.pagination import paginate_query

class OrderRepo:
    def __init__(self, db: Session):
        self.db = db

    def get(self, order_id: str) -> OrderRecord:
        return self.db.query(OrderRecord).filter(OrderRecord.order_id == order_id).first()

    def list_orders(self, skip: int = 0, limit: int = 100):
        query = self.db.query(OrderRecord)
        orders, pagination = paginate_query(query, limit=limit, offset=skip)
        return orders, pagination

    def create(self, order: OrderRecord) -> OrderRecord:
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def update(self, db_order: OrderRecord, update_data: dict) -> OrderRecord:
        for field, value in update_data.items():
            setattr(db_order, field, value)
        self.db.commit()
        self.db.refresh(db_order)
        return db_order

    def delete(self, db_order: OrderRecord):
        self.db.delete(db_order)
        self.db.commit()
        return True
