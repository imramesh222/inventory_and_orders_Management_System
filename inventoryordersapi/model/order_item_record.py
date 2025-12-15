from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from model import Base
from sqlalchemy import ForeignKey


class OrderItemRecord(Base):
    __tablename__ = "order_item"

    order_item_id = Column(String(255), primary_key=True)
    order_id = Column(String(255), ForeignKey("order.order_id"), nullable=False)
    item_id = Column(String(255), ForeignKey("item.item_id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Float, nullable=False)  # store price at time of order

    order = relationship("OrderRecord", back_populates="order_items")
    item = relationship("ItemRecord", back_populates="order_items")