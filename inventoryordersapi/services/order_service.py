from sqlalchemy.orm import Session
from repo.order_repo import OrderRepo
from repo.order_item_repo import OrderItemRepo
from repo.item_repo import ItemRepo
from model.order_record import OrderRecord
from model.order_item_record import OrderItemRecord
from domain.order_req_res import CreateOrderRequest
from utils.pagination import paginate_query
import uuid

class OrderService:
    def __init__(self, db: Session):
        self.db = db
        self.order_repo = OrderRepo(db)
        self.order_item_repo = OrderItemRepo(db)
        self.item_repo = ItemRepo(db)

    def get_order(self, order_id: str):
        return self.order_repo.get(order_id)


    def list_orders(self, skip: int = 0, limit: int = 100):
        query = self.db.query(OrderRecord)
        orders, pagination = paginate_query(query, limit=limit, offset=skip)
        return orders, pagination


    def create_order(self, order_data: CreateOrderRequest):
        total_amount = 0
        order_items_records = []

        for item_data in order_data.order_items:
            db_item = self.item_repo.get(item_data.item_id)
            if not db_item or db_item.item_quantity < item_data.quantity:
                raise ValueError(f"Item {item_data.item_id} not available or insufficient quantity")
            db_item.item_quantity -= item_data.quantity
            self.db.commit()
            total_amount += item_data.price * item_data.quantity

            order_item = OrderItemRecord(
                order_item_id=str(uuid.uuid4()),
                item_id=db_item.item_id,
                quantity=item_data.quantity,
                price=item_data.price
            )
            order_items_records.append(order_item)

        db_order = OrderRecord(
            order_id=str(uuid.uuid4()),
            customer_name=order_data.customer_name,
            customer_email=order_data.customer_email,
            total_amount=total_amount,
            is_paid=False,
            order_items=order_items_records
        )
        return self.order_repo.create(db_order)

    def update_order(self, order_id: str, update_data: dict):
        db_order = self.order_repo.get(order_id)
        if not db_order:
            return None
        return self.order_repo.update(db_order, update_data)

    def delete_order(self, order_id: str):
        db_order = self.order_repo.get(order_id)
        if not db_order:
            return None
        return self.order_repo.delete(db_order)
