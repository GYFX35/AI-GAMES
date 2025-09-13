import unittest
from unittest.mock import patch, MagicMock
import json
import os

# Add the parent directory to the Python path to allow importing from 'api'
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api import tiktok

class TestTikTok(unittest.TestCase):

    def setUp(self):
        # Create a dummy api_keys.json file for testing
        self.api_keys = {
            "tiktok": {
                "client_key": "test_client_key",
                "client_secret": "test_client_secret"
            }
        }
        with open("api/api_keys.json", "w") as f:
            json.dump(self.api_keys, f)

    def tearDown(self):
        # Clean up the dummy api_keys.json file
        if os.path.exists("api/api_keys.json"):
            os.remove("api/api_keys.json")

    @patch("api.tiktok.requests.post")
    def test_get_access_token(self, mock_post):
        # Mock the response from the TikTok API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"access_token": "test_access_token"}}
        mock_post.return_value = mock_response

        # Call the function
        result = tiktok.get_access_token("test_code")

        # Assert that the mock was called with the correct arguments
        mock_post.assert_called_once_with(
            f"{tiktok.TIKTOK_API_BASE_URL}/oauth/token/",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "client_key": "test_client_key",
                "client_secret": "test_client_secret",
                "code": "test_code",
                "grant_type": "authorization_code"
            }
        )

        # Assert that the function returns the correct value
        self.assertEqual(result, {"data": {"access_token": "test_access_token"}})

    @patch("api.tiktok.requests.get")
    def test_get_user_info(self, mock_get):
        # Mock the response from the TikTok API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"user": {"display_name": "Test User"}}}
        mock_get.return_value = mock_response

        # Call the function
        result = tiktok.get_user_info("test_access_token")

        # Assert that the mock was called with the correct arguments
        mock_get.assert_called_once_with(
            f"{tiktok.TIKTOK_API_BASE_URL}/user/info/?fields=open_id,union_id,avatar_url,display_name",
            headers={"Authorization": "Bearer test_access_token"}
        )

        # Assert that the function returns the correct value
        self.assertEqual(result, {"data": {"user": {"display_name": "Test User"}}})

    @patch("api.tiktok.requests.post")
    def test_get_video_list(self, mock_post):
        # Mock the response from the TikTok API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"videos": [{"id": "123"}]}}
        mock_post.return_value = mock_response

        # Call the function
        result = tiktok.get_video_list("test_access_token")

        # Assert that the mock was called with the correct arguments
        mock_post.assert_called_once_with(
            f"{tiktok.TIKTOK_API_BASE_URL}/video/list/?fields=id,title,video_description,duration,cover_image_url,embed_link",
            headers={
                "Authorization": "Bearer test_access_token",
                "Content-Type": "application/json"
            },
            json={"max_count": 20}
        )

        # Assert that the function returns the correct value
        self.assertEqual(result, {"data": {"videos": [{"id": "123"}]}})

if __name__ == "__main__":
    unittest.main()
