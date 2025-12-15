from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from model import Base

class OrderRecord(Base):
    __tablename__ = "order"

    order_id = Column(String(255), primary_key=True)
    customer_name = Column(String(255), nullable=False)
    customer_email = Column(String(255), nullable=False)
    total_amount = Column(Float, nullable=False, default=0.0)
    is_paid = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    order_items = relationship(
        "OrderItemRecord",
        back_populates="order",
        cascade="all, delete-orphan"
    )
