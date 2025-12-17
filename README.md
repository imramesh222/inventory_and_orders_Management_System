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

7. create database
    ```bash
    createdb inventoryordersapi
    ```
8. run migrations
    ```bash
    python -m inventoryordersapi.core.migrations.migrate
    ```

9. run the application
    ```bash
    uvicorn inventoryordersapi.main:app --reload
    ```

### link to postman collection
https://web.postman.co/workspace/ce03356f-39b6-48d4-86ae-9b2ca9fc3cb4/collection/41568675-71b65322-d8e7-438e-b8d3-e45d7f650057?action=share&source=copy-link&creator=41568675



### Swagger UI Collection

- `http://localhost:8000/docs`
screenshots of swagger ui collection
![swagger ui collection](/static/screenshots/Screenshot1.png)
![swagger ui collection](/static/screenshots/Screenshot2.png)
![swagger ui collection](/static/screenshots/Screenshot3.png)
![swagger ui collection](/static/screenshots/Screenshot4.png)
![swagger ui collection](/static/screenshots/Screenshot5.png)
![swagger ui collection](/static/screenshots/Screenshot6.png)
![swagger ui collection](/static/screenshots/Screenshot7.png)
![swagger ui collection](/static/screenshots/Screenshot8.png)
![swagger ui collection](/static/screenshots/Screenshot9.png)
![swagger ui collection](/static/screenshots/Screenshot10.png)
![swagger ui collection](/static/screenshots/Screenshot11.png)
![swagger ui collection](/static/screenshots/Screenshot12.png)
![swagger ui collection](/static/screenshots/Screenshot13.png)
![swagger ui collection](/static/screenshots/Screenshot14.png)
![swagger ui collection](/static/screenshots/Screenshot15.png)
![swagger ui collection](/static/screenshots/Screenshot16.png)
