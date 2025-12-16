from sqlalchemy.orm import Session
from domain.order_item import OrderItemRead, OrderItemCreate
from repo.order_repo import OrderRepo
from repo.order_item_repo import OrderItemRepo
from repo.item_repo import ItemRepo
from model.order_record import OrderRecord
from model.order_item_record import OrderItemRecord
from model.item_record import ItemRecord
from domain.order import OrderRead
from domain.order_req_res import (
    CreateOrderRequest, CreateOrderResponse, 
    UpdateOrderRequest, UpdateOrderResponse,
    GetOrderResponse, ListOrderResponse
)
from domain.common import ErrorCode
from utils.pagination import paginate_query
from typing import List, Optional
from datetime import datetime

class OrderService:
    def __init__(self, db: Session):
        self.db = db
        self.order_repo = OrderRepo(db)
        self.order_item_repo = OrderItemRepo(db)
        self.item_repo = ItemRepo(db)

    def get_order(self, order_id: str) -> GetOrderResponse:
        """Get order by ID"""
        try:
            order = self.order_repo.get(order_id)
            if not order:
                return GetOrderResponse(
                    error=True,
                    code=ErrorCode.NOT_FOUND,
                    msg=f"Order with ID {order_id} not found"
                )
            return GetOrderResponse(
                order=order,
                msg="Order retrieved successfully"
            )
        except Exception as e:
            return GetOrderResponse(
                error=True,
                code=ErrorCode.INTERNAL_ERROR,
                msg=str(e)
            )

    def list_orders(self, skip: int = 0, limit: int = 100) -> ListOrderResponse:
        """List orders with pagination"""
        try:
            query = self.db.query(OrderRecord)
            orders, pagination = paginate_query(query, limit=limit, offset=skip)
            return ListOrderResponse(
                orders=orders,
                pagination=pagination,
                msg="Orders listed successfully"
            )
        except Exception as e:
            return ListOrderResponse(
                error=True,
                code=ErrorCode.INTERNAL_ERROR,
                msg=str(e)
            )

    def create_order(self, request: CreateOrderRequest) -> CreateOrderResponse:
        """Create a new order with items"""
        try:
            order_data = request.order
            # Start a transaction
            with self.db.begin():
                # Create order record
                order_record = OrderRecord(
                    customer_name=order_data.customer_name,
                    customer_email=order_data.customer_email,
                    total_amount=0,  # Will be calculated
                    is_paid=False
                )
                self.db.add(order_record)
                self.db.flush()  # To get the order_id

                total_amount = 0
                order_items = []

                # Process each order item
                for item in order_data.order_items:
                    # Get item with lock to prevent race conditions
                    db_item = self.db.query(ItemRecord).filter(
                        ItemRecord.item_id == item.item_id
                    ).with_for_update().first()

                    if not db_item:
                        self.db.rollback()
                        return CreateOrderResponse(
                            error=True,
                            code=ErrorCode.NOT_FOUND,
                            msg=f"Item with ID {item.item_id} not found"
                        )

                    # Check stock
                    if db_item.item_quantity < item.quantity:
                        self.db.rollback()
                        return CreateOrderResponse(
                            error=True,
                            code=ErrorCode.INSUFFICIENT_STOCK,
                            msg=f"Insufficient stock for item {db_item.item_name}"
                        )

                    # Calculate item total
                    item_total = db_item.item_price * item.quantity
                    total_amount += item_total

                    # Create order item
                    order_item = OrderItemRecord(
                        order_id=order_record.order_id,
                        item_id=item.item_id,
                        quantity=item.quantity,
                        price=db_item.item_price
                    )
                    self.db.add(order_item)
                    order_items.append(order_item)

                    # Update item quantity
                    db_item.item_quantity -= item.quantity
                    self.db.add(db_item)

                # Update order total
                order_record.total_amount = total_amount
                self.db.add(order_record)

                # Convert to Pydantic model for response
                order_read = OrderRead(
                    order_id=order_record.order_id,
                    customer_name=order_record.customer_name,
                    customer_email=order_record.customer_email,
                    total_amount=order_record.total_amount,
                    is_paid=order_record.is_paid,
                    created_at=order_record.created_at,
                    updated_at=order_record.updated_at,
                    order_items=[
                        OrderItemRead(
                            order_item_id=item.order_item_id,
                            item_id=item.item_id,
                            quantity=item.quantity,
                            price=item.price,
                            created_at=item.created_at,
                            updated_at=item.updated_at
                        ) for item in order_items
                    ]
                )

                return CreateOrderResponse(
                    order=order_read,
                    msg="Order created successfully"
                )

        except Exception as e:
            self.db.rollback()
            return CreateOrderResponse(
                error=True,
                code=ErrorCode.INTERNAL_ERROR,
                msg=str(e)
            )

    def update_order(self, order_id: str, request: UpdateOrderRequest) -> UpdateOrderResponse:
        """Update an existing order"""
        try:
            with self.db.begin():
                # Get existing order with items
                order = self.order_repo.get_for_update(order_id)
                if not order:
                    return UpdateOrderResponse(
                        error=True,
                        code=ErrorCode.NOT_FOUND,
                        msg=f"Order with ID {order_id} not found"
                    )

                # Update order fields
                update_data = request.dict(exclude_unset=True)
                for field, value in update_data.items():
                    if hasattr(order, field) and field != 'order_items':
                        setattr(order, field, value)

                # If updating order items, handle carefully
                if 'order_items' in update_data:
                    # For simplicity, we'll just update the entire order
                    # In a real app, you'd want to handle this more carefully
                    # by calculating diffs and updating quantities accordingly
                    pass

                self.db.add(order)
                return UpdateOrderResponse(
                    order=order,
                    msg="Order updated successfully"
                )

        except Exception as e:
            self.db.rollback()
            return UpdateOrderResponse(
                error=True,
                code=ErrorCode.INTERNAL_ERROR,
                msg=str(e)
            )

    def delete_order(self, order_id: str) -> bool:
        """Delete an order"""
        try:
            with self.db.begin():
                order = self.order_repo.get(order_id)
                if not order:
                    return False
                self.order_repo.delete(order)
                return True
        except Exception:
            self.db.rollback()
            return False