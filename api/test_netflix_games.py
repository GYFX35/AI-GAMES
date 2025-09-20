import unittest
from fastapi.testclient import TestClient
from api.main import app

class TestNetflixGames(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        # You might need to set up a test API key if your endpoint is protected
        self.api_key = "test-api-key"  # Replace with a valid test key if needed
        self.headers = {"X-API-Key": self.api_key}

    def test_get_netflix_games(self):
        """
        Test that the /api/netflix/games endpoint returns a list of games.
        """
        # Make a request to the endpoint
        response = self.client.get("/api/netflix/games", headers=self.headers)

        # Assert that the response is successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response contains a list of games
        games = response.json()
        self.assertIsInstance(games, list)
        if games:
            self.assertIn("title", games[0])
            self.assertIn("description", games[0])

if __name__ == '__main__':
    unittest.main()
