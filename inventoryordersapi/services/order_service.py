from sqlalchemy.orm import Session
from inventoryordersapi.domain.order_item import OrderItemRead, OrderItemCreate
from inventoryordersapi.domain.order_response import OrderItemResponse, OrderResponse
from inventoryordersapi.repo.order_repo import OrderRepo
from inventoryordersapi.repo.order_item_repo import OrderItemRepo
from inventoryordersapi.repo.item_repo import ItemRepo
from inventoryordersapi.model.order_record import OrderRecord
from inventoryordersapi.model.order_item_record import OrderItemRecord
from inventoryordersapi.model.item_record import ItemRecord
from inventoryordersapi.domain.order import OrderRead
from inventoryordersapi.domain.order_req_res import (
    CreateOrderRequest, CreateOrderResponse, 
    UpdateOrderRequest, UpdateOrderResponse,
    GetOrderResponse, ListOrderResponse
)
from inventoryordersapi.domain.common import ErrorCode
from inventoryordersapi.utils.pagination import paginate_query
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

    def list_orders(
        self,
        customer_name: str | None = None,
        status: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        page: int = 1,
        page_size: int = 10
    ):
        query = self.db.query(OrderRecord)

        if customer_name:
            query = query.filter(OrderRecord.customer_name.ilike(f"%{customer_name}%"))
        
        if status:
            if status.lower() == "confirmed":
                query = query.filter(OrderRecord.status == "confirmed")
            elif status.lower() == "unpaid":
                query = query.filter(OrderRecord.status != "confirmed")
    
        if from_date:
            from_dt = datetime.fromisoformat(from_date)
            query = query.filter(OrderRecord.created_at >= from_dt)
    
        if to_date:
            to_dt = datetime.fromisoformat(to_date)
            query = query.filter(OrderRecord.created_at <= to_dt)

        offset = (page - 1) * page_size
        orders, pagination = paginate_query(query, limit=page_size, offset=offset, page=page, page_size=page_size)
    
        # Convert OrderRecord to OrderRead
        orders_read = []
        for order in orders:
                orders_read.append(OrderRead(
                order_id=order.order_id,
                customer_name=order.customer_name,
                customer_email=order.customer_email,
                total_amount=order.total_amount,
                status=order.status,
                created_at=order.created_at,
                updated_at=order.updated_at,
                order_items=[OrderItemRead(
                    order_item_id=item.order_item_id,
                    item_id=item.item_id,
                    quantity=item.quantity,
                    price=item.price,
                    created_at=item.created_at,
                    updated_at=item.updated_at
                ) for item in order.order_items]
            ))

        return orders_read, pagination

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
                    status="pending"
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
                    status=order_record.status,
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

    def cancel_order(self, order_id: str) -> bool:
        """
        Cancel an order. Restores stock if needed.
            """
        try:
            with self.db.begin():
                order = self.order_repo.get_for_update(order_id)
                if not order:
                    return False  # Order not found
                if order.status == "canceled":
                    return False
                if order.status == "confirmed":
                    return False
                # Mark order as canceled
                order.status = "canceled"
                self.db.add(order)

                # Restore stock
                for item in order.order_items:
                    db_item = self.item_repo.get_for_update(item.item_id)
                    if db_item:
                        db_item.item_quantity += item.quantity
                        self.db.add(db_item)

            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Error canceling order {order_id}: {e}")
            return False

    def format_order_response(self, order_read: OrderRead) -> OrderResponse:
        items = [
            OrderItemResponse(
                item_id=item.item_id,
                name=getattr(item, "item_name", getattr(item, "price", "")),  # if you have item name somewhere
                unit_price=item.price,
                quantity=item.quantity,
                line_total=item.price * item.quantity
            )
            for item in order_read.order_items
        ]

        return OrderResponse(
            id=order_read.order_id,
            customer_name=order_read.customer_name,
            status=order_read.status,
            total_amount=order_read.total_amount,
            created_at=order_read.created_at.isoformat() if hasattr(order_read.created_at, "isoformat") else str(order_read.created_at),
        items=items
    )


    def format_order_items_for_response(self, order_read: OrderRead):
        """
        Convert internal OrderItemRead to API-friendly format (unit_price, line_total, name)
        """
        formatted_items = []
        for item in order_read.order_items:
            # get item name if item object exists, else fallback
            item_name = getattr(item, "item_name", None)
            if not item_name and hasattr(item, "item") and getattr(item.item, "item_name", None):
                item_name = item.item.item_name
            formatted_items.append({
                "item_id": item.item_id,
                "name": item_name or "Unknown",
                "unit_price": item.price,
                "quantity": item.quantity,
                "line_total": item.price * item.quantity
            })
        return formatted_items

    def format_order_for_response(self, order_read: OrderRead):
        """
        Convert OrderRead to dict matching spec example
        """
        return {
            "id": order_read.order_id,
            "customer_name": order_read.customer_name,
            "status": order_read.status,
            "total_amount": order_read.total_amount,
            "created_at": order_read.created_at.isoformat(),
            "items": self.format_order_items_for_response(order_read)
        }



