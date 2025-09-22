import unittest
from unittest.mock import patch, Mock
from fastapi.testclient import TestClient
from api.main import app

class TestUnicornAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.api_key = "test-api-key"
        self.headers = {"X-API-Key": self.api_key}

    @patch('api.unicorn.API_KEY', "fake-api-key")
    @patch('requests.get')
    def test_translate_for_unicorn(self, mock_get):
        # Mock the response from the fun translations API
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": {"total": 1},
            "contents": {
                "translated": "a unicorn-friendly dialect, translated text is.",
                "text": "this is the text to be translated.",
                "translation": "yoda"
            }
        }
        mock_get.return_value = mock_response

        # Call the endpoint
        response = self.client.post(
            "/api/unicorn/translate",
            headers=self.headers,
            json={"text": "this is the text to be translated."}
        )

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['contents']['translated'], "a unicorn-friendly dialect, translated text is.")

    @patch('api.unicorn.API_KEY', None)
    def test_translate_for_unicorn_no_api_key(self):

        # Call the endpoint
        response = self.client.post(
            "/api/unicorn/translate",
            headers=self.headers,
            json={"text": "this is the text to be translated."}
        )

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertIn("Translated: ", response.json()['contents']['translated'])
