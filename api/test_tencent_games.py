import pytest
from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

API_KEY = "test-api-key"
HEADERS = {"X-API-Key": API_KEY}

def test_get_tencent_games_success():
    response = client.get("/api/tencent/games", headers=HEADERS)
    assert response.status_code == 200
    assert len(response.json()) == 3

def test_get_tencent_games_no_api_key():
    response = client.get("/api/tencent/games")
    assert response.status_code == 403
    assert response.json()["detail"] == "Not authenticated"
