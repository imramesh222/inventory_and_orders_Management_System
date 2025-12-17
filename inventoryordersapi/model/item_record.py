from sqlalchemy import Column, String, Float, Integer, Boolean, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from inventoryordersapi.model import Base
import uuid

class ItemRecord(Base):
    __tablename__ = "item"

    item_id = Column(String(255), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    item_name = Column(String(255), nullable=False)  # Added back item_name
    item_description = Column(Text, nullable=True)
    item_price = Column(Float, nullable=False)
    item_quantity = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)   
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    order_items = relationship(
        "OrderItemRecord",
        back_populates="item",
        cascade="all, delete-orphan"
    )