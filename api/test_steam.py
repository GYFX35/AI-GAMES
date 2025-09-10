import unittest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch

class TestSteam(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.api_key = "test-api-key"
        self.headers = {"X-API-Key": self.api_key}

    def get_mock_steam_games(self):
        return {
            "applist": {
                "apps": [
                    {"appid": 570, "name": "Dota 2"},
                    {"appid": 730, "name": "Counter-Strike: Global Offensive"},
                    {"appid": 440, "name": "Team Fortress 2"},
                ]
            }
        }

    def test_get_steam_games_success(self):
        with patch("steam.requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = self.get_mock_steam_games()

            response = self.client.get("/api/steam/games", headers=self.headers)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.json()), 3)

    def test_get_steam_games_no_api_key(self):
        response = self.client.get("/api/steam/games")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()["detail"], "Not authenticated")
