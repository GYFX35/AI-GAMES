import unittest
from unittest.mock import patch, Mock
from fastapi.testclient import TestClient
from api.main import app

class TestMakeupAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.api_key = "test-api-key"
        self.headers = {"X-API-Key": self.api_key}

    @patch('requests.get')
    def test_get_makeup_products(self, mock_get):
        # Mock the response from the makeup API
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": 1, "name": "Test Lipstick"}]
        mock_get.return_value = mock_response

        # Call the endpoint
        response = self.client.get("/api/makeup/products", headers=self.headers)

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{"id": 1, "name": "Test Lipstick"}])

    @patch('requests.get')
    def test_get_makeup_products_with_filter(self, mock_get):
        # Mock the response from the makeup API
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": 2, "name": "Test Foundation", "brand": "maybelline"}]
        mock_get.return_value = mock_response

        # Call the endpoint with a filter
        response = self.client.get("/api/makeup/products?brand=maybelline", headers=self.headers)

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{"id": 2, "name": "Test Foundation", "brand": "maybelline"}])

        # Assert that requests.get was called with the correct parameters
        mock_get.assert_called_with(
            "http://makeup-api.herokuapp.com/api/v1/products.json",
            params={"brand": "maybelline"}
        )
