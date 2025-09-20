import unittest
from fastapi.testclient import TestClient
from api.main import app

class TestJungleeGames(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.api_key = "test-api-key"
        self.headers = {"X-API-Key": self.api_key}

    def test_get_junglee_games(self):
        """
        Test that the /api/junglee/games endpoint returns a list of games.
        """
        response = self.client.get("/api/junglee/games", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        games = response.json()
        self.assertIsInstance(games, list)
        if games:
            self.assertIn("title", games[0])
            self.assertIn("description", games[0])

if __name__ == '__main__':
    unittest.main()
