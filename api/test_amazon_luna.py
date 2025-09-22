import unittest
from fastapi.testclient import TestClient
from api.main import app

class TestAmazonLuna(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.api_key = "test-api-key"
        self.headers = {"X-API-Key": self.api_key}

    def test_get_amazon_luna_games_success(self):
        response = self.client.get("/api/amazon-luna/games", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    def test_get_amazon_luna_games_no_api_key(self):
        response = self.client.get("/api/amazon-luna/games")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()["detail"], "Not authenticated")
