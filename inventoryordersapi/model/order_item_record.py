from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from inventoryordersapi.model import Base
import uuid
class OrderItemRecord(Base):
    __tablename__ = "order_item"
    order_item_id = Column(String(255), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = Column(String(255), ForeignKey("order.order_id"), nullable=False)
    item_id = Column(String(255), ForeignKey("item.item_id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Float, nullable=False)  # store price at time of order
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    order = relationship("OrderRecord", back_populates="order_items")
    item = relationship("ItemRecord", back_populates="order_items")

    def __init__(self, **kwargs):
        if 'order_item_id' not in kwargs:
            kwargs['order_item_id'] = str(uuid.uuid4())
        super().__init__(**kwargs)