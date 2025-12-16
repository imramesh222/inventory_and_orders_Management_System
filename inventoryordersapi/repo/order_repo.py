from typing import List, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from model.order_record import OrderRecord
from model.order_item_record import OrderItemRecord
from domain.order import Order, OrderRead
from domain.order_item import OrderItemRead, OrderItemCreate
from utils.pagination import paginate_query

class OrderRepo:
    def __init__(self, db: Session):
        self.db = db

    def _record_to_order_item(self, record: OrderItemRecord) -> OrderItemRead:
        """Convert OrderItemRecord to OrderItemRead"""
        if not record:
            return None
        
        from domain.item import ItemRead
        
        return OrderItemRead(
            order_item_id=str(record.order_item_id),
            item_id=str(record.item_id),
            quantity=record.quantity,
            price=record.price,
            created_at=record.created_at if hasattr(record, 'created_at') else None,
            updated_at=record.updated_at if hasattr(record, 'updated_at') else None,
            item=ItemRead(
                item_id=str(record.item.item_id),
                item_name=record.item.item_name,
                item_description=record.item.item_description,
                item_price=record.item.item_price,
                item_quantity=record.item.item_quantity,
                is_active=record.item.is_active,
                created_at=record.item.created_at,
                updated_at=record.item.updated_at
            ) if record.item else None
        )

    def _record_to_order_read(self, record: OrderRecord) -> OrderRead:
        """Convert OrderRecord (SQLAlchemy) to OrderRead (Pydantic)"""
        if not record:
            return None
        
        # Convert order items
        order_items = [
            self._record_to_order_item(item)
            for item in record.order_items
        ] if record.order_items else []
        
        return OrderRead(
            order_id=str(record.order_id),
            customer_name=record.customer_name,
            customer_email=record.customer_email,
            total_amount=record.total_amount,
            is_paid=record.is_paid,
            order_items=order_items,
            created_at=record.created_at,
            updated_at=record.updated_at
        )

    def get(self, order_id: str) -> OrderRead:
        record = self.db.query(OrderRecord).filter(OrderRecord.order_id == order_id).first()
        return self._record_to_order_read(record)

    def list_orders(self, skip: int = 0, limit: int = 100):
        query = self.db.query(OrderRecord)
        records, pagination = paginate_query(query, limit=limit, offset=skip)
        orders = [self._record_to_order_read(record) for record in records]
        return orders, pagination

    def create(self, order_data: Dict[str, Any]) -> OrderRead:
        """Create a new order with order items in a transaction"""
        try:
            with self.db.begin():
                # Create order
                order = OrderRecord(
                    customer_name=order_data['customer_name'],
                    customer_email=order_data['customer_email'],
                    total_amount=order_data['total_amount'],
                    is_paid=False
                )
                self.db.add(order)
                self.db.flush()  # Get the order_id
                
                # Create order items
                for item_data in order_data['items']:
                    order_item = OrderItemRecord(
                        order_id=order.order_id,
                        item_id=item_data["item_id"],
                        quantity=item_data["quantity"],
                        price=item_data["price"]
                    )
                    self.db.add(order_item)
                
                self.db.refresh(order)
                return self._record_to_order_read(order)
                
        except Exception as e:
            self.db.rollback()
            raise e

    def update(self, db_order: OrderRecord, update_data: dict) -> OrderRead:
        with self.db.begin():
            for field, value in update_data.items():
                if field != 'order_id' and hasattr(db_order, field):
                    setattr(db_order, field, value)
            self.db.refresh(db_order)
            return self._record_to_order_read(db_order)

    def delete(self, db_order: OrderRecord) -> bool:
        with self.db.begin():
            self.db.delete(db_order)
            return True