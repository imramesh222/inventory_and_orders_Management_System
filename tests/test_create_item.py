import pytest
def test_create_item(client):
    payload = {
        "item": {
            "item_name": "Keyboard",
            "item_description": "Mechanical keyboard",
            "item_price": 2500.0,
            "item_quantity": 10,
            "low_stock": False
        }
    }
    response = client.post("/items/add_item", json=payload, headers={"X-API-KEY": "rameshapikey"})
    assert response.status_code == 200
    data = response.json()
    assert "item" in data
    assert data["item"]["item_name"] == "Keyboard"
    print(response.json())
