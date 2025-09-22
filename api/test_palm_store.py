import unittest
from fastapi.testclient import TestClient
from api.main import app

class TestPalmStore(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.api_key = "test-api-key"
        self.headers = {"X-API-Key": self.api_key}

    def test_get_palm_store_games_success(self):
        response = self.client.get("/api/palm/games", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    def test_get_palm_store_game_by_id_success(self):
        response = self.client.get("/api/palm/games/1", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        game = response.json()
        self.assertEqual(game["id"], 1)
        self.assertEqual(game["name"], "Palm Racer")

    def test_get_palm_store_game_by_id_not_found(self):
        response = self.client.get("/api/palm/games/999", headers=self.headers)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Game not found in Palm Store.")

    def test_get_palm_store_games_no_api_key(self):
        response = self.client.get("/api/palm/games")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()["detail"], "Not authenticated")
