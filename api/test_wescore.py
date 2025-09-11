import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, MagicMock
from api import wescore
import requests

class TestWeScore(unittest.TestCase):

    @patch('api.wescore.API_KEY', 'test_key')
    @patch('api.wescore.API_SECRET', 'test_secret')
    @patch('api.wescore.requests.get')
    def test_get_live_scores_success(self, mock_get):
        # Mock the API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"live": "scores"}}
        mock_get.return_value = mock_response

        # Call the function
        result = wescore.get_live_scores()

        # Assert the result
        self.assertEqual(result, {"data": {"live": "scores"}})

    @patch('api.wescore.API_KEY', 'test_key')
    @patch('api.wescore.API_SECRET', 'test_secret')
    @patch('api.wescore.requests.get')
    def test_get_live_scores_failure(self, mock_get):
        # Mock the API response
        mock_get.side_effect = requests.exceptions.RequestException("API is down")

        # Call the function
        result = wescore.get_live_scores()

        # Assert the result
        self.assertIsNone(result)

    @patch('api.wescore.API_KEY', 'YOUR_WESCORE_API_KEY')
    def test_get_live_scores_no_credentials(self):
        # Call the function
        result = wescore.get_live_scores()

        # Assert the result
        self.assertEqual(result, {"error": "API key and secret not set for WeScore."})

    @patch('api.wescore.API_KEY', 'test_key')
    @patch('api.wescore.API_SECRET', 'test_secret')
    @patch('api.wescore.requests.get')
    def test_get_all_fixtures_success(self, mock_get):
        # Mock the API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"fixtures": "list"}}
        mock_get.return_value = mock_response

        # Call the function
        result = wescore.get_all_fixtures()

        # Assert the result
        self.assertEqual(result, {"data": {"fixtures": "list"}})

if __name__ == '__main__':
    unittest.main()
