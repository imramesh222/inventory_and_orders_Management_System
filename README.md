# 📦 Inventory & Orders Management System

A robust RESTful API for managing inventory and processing orders with proper stock management, built with FastAPI and PostgreSQL.

## 🚀 Features

### Inventory Management
- ✅ Create, read, update, and delete items
- ✅ Track item quantities and prices
- ✅ Filter and search items
- ✅ Paginated item listings

### Order Processing
- 🛒 Create and manage customer orders
- 📉 Automatic stock level updates
- 🔄 Transaction management for data consistency
- 📊 Order history and tracking

### API Endpoints

#### Items
- `GET /items` - List all items (paginated)
- `POST /items` - Create a new item
- `GET /items/{item_id}` - Get item details
- `PUT /items/{item_id}` - Update an item
- `DELETE /items/{item_id}` - Delete an item

#### Orders
- `POST /orders` - Create a new order
- `GET /orders/{order_id}` - Get order details
- `GET /orders` - List all orders (paginated)

## 🛠️ Tech Stack

- **Backend Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Containerization**: Docker (optional)
- **Testing**: Pytest

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL
- Pip

### Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/yourusername/inventory_and_orders_Management_System.git](https://github.com/yourusername/inventory_and_orders_Management_System.git)
   cd inventory_and_orders_Management_System