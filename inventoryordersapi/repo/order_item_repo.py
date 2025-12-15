from sqlalchemy.orm import Session
from model.order_item_record import OrderItemRecord
from domain.order_item import OrderItemRead

class OrderItemRepo:
    def __init__(self, db: Session):
        self.db = db

    def _record_to_order_item(self, record: OrderItemRecord) -> OrderItemRead:
        """Convert OrderItemRecord (SQLAlchemy) to OrderItemRead (Pydantic)"""
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

    def create(self, order_item: OrderItemRecord) -> OrderItemRead:
        self.db.add(order_item)
        self.db.commit()
        self.db.refresh(order_item)
        return self._record_to_order_item(order_item)

    def delete(self, db_order_item: OrderItemRecord):
        self.db.delete(db_order_item)
        self.db.commit()
        return True