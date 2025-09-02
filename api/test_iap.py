import pytest
from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

API_KEY = "test-api-key"
HEADERS = {"X-API-Key": API_KEY}

def test_get_iap_products_success():
    response = client.get("/api/iap/products", headers=HEADERS)
    assert response.status_code == 200
    assert len(response.json()) == 3

def test_verify_purchase_success():
    purchase_data = {
        "productId": "com.supergame.coins_100",
        "purchaseToken": "some_long_purchase_token"
    }
    response = client.post("/api/iap/verify-purchase", json=purchase_data, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["product_id"] == "com.supergame.coins_100"

def test_get_iap_products_no_api_key():
    response = client.get("/api/iap/products")
    assert response.status_code == 403
    assert response.json()["detail"] == "Not authenticated"
