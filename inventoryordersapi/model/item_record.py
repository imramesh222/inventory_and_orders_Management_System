from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from model import Base

class ItemRecord(Base):
    __tablename__ = "item"

    item_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    item_name = Column(String(255), nullable=False)
    item_description = Column(Text, nullable=True)
    item_price = Column(Float, nullable=False)
    item_quantity = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)   
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    order_items = relationship(
        "OrderItemRecord",
        back_populates="item",
        cascade="all, delete-orphan"
    )
