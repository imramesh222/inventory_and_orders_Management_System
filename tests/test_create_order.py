import pytest
def test_create_order(client):

    payload = {
        "item": {
            "item_name": "Keyboard",
            "item_description": "Mechanical keyboard",
            "item_price": 2500.0,
            "item_quantity": 10,
            "low_stock": False
        }
    }
    item_response = client.post("/items/add_item", json=payload, headers={"X-API-KEY": "rameshapikey"})
    assert item_response.status_code == 200
    item_id = item_response.json()["item"]["item_id"]

    # Then create the order
    order_payload = {
        "order": {
            "customer_name": "John Doe",
            "customer_email": "john@example.com",
            "order_items": [
                {"item_id": item_id, "quantity": 2}
            ]
        }
    }
    order_response = client.post("/orders/", json=order_payload, headers={"X-API-KEY": "rameshapikey"})
    assert order_response.status_code == 200
    data = order_response.json()
    assert data["order"]["customer_name"] == "John Doe"
    print(order_response.status_code)
    print(order_response.json())
    print(item_response.status_code, item_response.json())
