import pytest
from fastapi.testclient import TestClient
from .main import app
from unittest.mock import patch

client = TestClient(app)

API_KEY = "test-api-key"
HEADERS = {"X-API-Key": API_KEY}

def get_mock_steam_games():
    return {
        "applist": {
            "apps": [
                {"appid": 570, "name": "Dota 2"},
                {"appid": 730, "name": "Counter-Strike: Global Offensive"},
                {"appid": 440, "name": "Team Fortress 2"},
            ]
        }
    }

def test_get_steam_games_success():
    with patch("api.steam.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = get_mock_steam_games()

        response = client.get("/api/steam/games", headers=HEADERS)
        assert response.status_code == 200
        assert len(response.json()) == 3

def test_get_steam_games_no_api_key():
    response = client.get("/api/steam/games")
    assert response.status_code == 403
    assert response.json()["detail"] == "Not authenticated"
