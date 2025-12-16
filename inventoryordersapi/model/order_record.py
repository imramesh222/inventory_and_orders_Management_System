from sqlalchemy import Column, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from model import Base
import uuid

class OrderRecord(Base):
    __tablename__ = "order"

    order_id = Column(String(255), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    customer_name = Column(String(255), nullable=False)
    customer_email = Column(String(255), nullable=False)
    total_amount = Column(Float, nullable=False, default=0.0)
    is_paid = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    order_items = relationship(
        "OrderItemRecord",
        back_populates="order",
        cascade="all, delete-orphan"
    )