import unittest
from fastapi.testclient import TestClient
from api.main import app, get_api_key
from unittest.mock import patch

import json
import os
class TestUnesco(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.api_key = "test-api-key"
        self.headers = {"X-API-Key": self.api_key}

    def get_mock_unesco_datasets(self):
        return {"datasets": [{"dataset": {"dataset_id": "mock_id"}}]}

    def get_mock_unesco_records(self, dataset_id):
        return {"records": [{"id": "1", "value": "mock_value"}]}

    def test_get_unesco_datasets(self):
        """
        Test the /api/unesco/datasets endpoint with a mock.
        """
        with patch("api.unesco.get_datasets", return_value=self.get_mock_unesco_datasets()):
            response = self.client.get("/api/unesco/datasets", headers=self.headers)
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("datasets", data)
            self.assertGreater(len(data["datasets"]), 0)

    def test_get_unesco_records(self):
        """
        Test the /api/unesco/datasets/{dataset_id}/records endpoint with a mock.
        """
        dataset_id = "mock_id"
        with patch("api.unesco.get_records", return_value=self.get_mock_unesco_records(dataset_id)):
            response = self.client.get(f"/api/unesco/datasets/{dataset_id}/records", headers=self.headers)
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("records", data)

    def test_unesco_ml_predict(self):
        """
        Test the /api/unesco/ml/predict endpoint.
        """
        dataset_id = "mock_id"
        with patch("api.unesco.get_records", return_value=self.get_mock_unesco_records(dataset_id)):
            request_body = {"dataset_id": dataset_id}
            response = self.client.post("/api/unesco/ml/predict", json=request_body, headers=self.headers)
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("mock_prediction", data)
