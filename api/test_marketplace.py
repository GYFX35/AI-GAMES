import pytest
from fastapi.testclient import TestClient
from api.main import app
import os
import json

client = TestClient(app)

@pytest.fixture
def api_key_headers():
    return {"X-API-Key": "test-api-key"}

def test_list_marketplace_items():
    response = client.get("/api/marketplace/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_marketplace_item(api_key_headers):
    new_item = {
        "name": "Test Item",
        "category": "Test",
        "price": 100,
        "description": "Test description",
        "image": "http://example.com/test.png"
    }
    response = client.post("/api/marketplace/", json=new_item, headers=api_key_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"
    assert "id" in data

    # Clean up
    item_id = data["id"]
    client.delete(f"/api/marketplace/{item_id}", headers=api_key_headers)

def test_get_dynamic_offers():
    response = client.get("/api/marketplace/offers/dynamic?user_segment=whale")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for item in data:
        assert item["price"] > 1000 or not data # if no items > 1000

def test_get_dynamic_offers_grinder():
    response = client.get("/api/marketplace/offers/dynamic?user_segment=grinder")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for item in data:
        assert item["category"] == "Tools"
