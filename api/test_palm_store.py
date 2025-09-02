import pytest
from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

# The API key is defined in `api/api_keys.json`
API_KEY = "test-api-key"
HEADERS = {"X-API-Key": API_KEY}

def test_get_palm_store_games_success():
    response = client.get("/api/palm/games", headers=HEADERS)
    assert response.status_code == 200
    assert len(response.json()) == 3

def test_get_palm_store_game_by_id_success():
    response = client.get("/api/palm/games/1", headers=HEADERS)
    assert response.status_code == 200
    game = response.json()
    assert game["id"] == 1
    assert game["name"] == "Palm Racer"

def test_get_palm_store_game_by_id_not_found():
    response = client.get("/api/palm/games/999", headers=HEADERS)
    assert response.status_code == 404
    assert response.json()["detail"] == "Game not found in Palm Store."

def test_get_palm_store_games_no_api_key():
    response = client.get("/api/palm/games")
    assert response.status_code == 403
    assert response.json()["detail"] == "Not authenticated"
