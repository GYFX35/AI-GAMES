import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from api.main import app

class TestMain(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.api_key = "test-api-key"
        self.headers = {"X-API-Key": self.api_key}

    def test_get_ai_action(self):
        """
        Test the /api/hockey/ai/action endpoint.
        """
        game_state = {"puck_owner": "player"}
        response = self.client.post("/api/hockey/ai/action", json=game_state, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("action", data)
        self.assertIn(data["action"], ["skate_back", "check_player", "block_shot"])

        game_state = {"puck_owner": "ai"}
        response = self.client.post("/api/hockey/ai/action", json=game_state, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("action", data)
        self.assertIn(data["action"], ["skate_forward", "pass_puck", "shoot_puck"])

    def test_get_nft_details(self):
        """
        Test the /api/hockey/nft/{token_id} endpoint.
        """
        # Test with a valid token ID
        token_id = 1
        response = self.client.get(f"/api/hockey/nft/{token_id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("owner", data)
        self.assertIn("uri", data)

        # Test with an invalid token ID
        token_id = 999
        response = self.client.get(f"/api/hockey/nft/{token_id}", headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_xcode_generate(self):
        """
        Test the /api/xcode/generate endpoint.
        """
        # Test with a prompt that should trigger the "network" template
        request_body = {"prompt": "network"}
        response = self.client.post("/api/xcode/generate", json=request_body, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertIn("code", response_json)
        self.assertIn("URLSession", response_json["code"])

        # Test with a prompt that should trigger the "default" template
        request_body = {"prompt": "unknown"}
        response = self.client.post("/api/xcode/generate", json=request_body, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertIn("code", response_json)
        self.assertIn("Hello, World!", response_json["code"])

    def test_facebook_webhook(self):
        """
        Test the /api/facebook/webhook endpoint.
        It should call the send_server_event function.
        """
        # Mock the send_server_event function to avoid real API calls
        with patch('api.fb_business.send_server_event') as mock_send_event:
            user_data = {"name": "Test User", "email": "test@example.com"}

            # The webhook endpoint does not require an API key
            response = self.client.post("/api/facebook/webhook", json=user_data)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"status": "success", "message": "Event processed"})

            # Verify that our mocked function was called once with the correct data
            mock_send_event.assert_called_once_with(user_data)

    def test_delete_game_not_found(self):
        """
        Test deleting a game that does not exist.
        """
        response = self.client.delete("/api/games/non_existent_game", headers=self.headers)
        self.assertEqual(response.status_code, 404)
