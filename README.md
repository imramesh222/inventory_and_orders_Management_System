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
- `PUT /orders/{order_id}` - Update an order
- `DELETE /orders/{order_id}` - Delete an order

## 🛠️ Tech Stack

- **Backend Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Migrations**: Liquibase

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL
- Pip

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/imramesh222/inventory_and_orders_Management_System.git
   ```
2. cd inventory_and_orders_Management_System
3. create virtual environment
    ```bash
    python -m venv venv
    ```
4. activate virtual environment
    ```bash
    source venv/bin/activate
    ```
5. install dependencies
    ```bash
    pip install -r requirements.txt
    ```
6. run the application
    ```bash
    uvicorn inventoryordersapi.main:app --reload
    ```