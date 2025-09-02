import pytest
from fastapi.testclient import TestClient
from .main import app, get_api_key
from unittest.mock import patch

client = TestClient(app)

API_KEY = "test-api-key"
HEADERS = {"X-API-Key": API_KEY}

# Helper function to get a mocked successful response for UNESCO datasets
def get_mock_unesco_datasets():
    return {"datasets": [{"dataset": {"dataset_id": "mock_id"}}]}

# Helper function to get a mocked successful response for UNESCO records
def get_mock_unesco_records(dataset_id):
    return {"records": [{"id": "1", "value": "mock_value"}]}

def test_get_unesco_datasets():
    """
    Test the /api/unesco/datasets endpoint with a mock.
    """
    with patch("api.unesco.get_datasets", return_value=get_mock_unesco_datasets()):
        response = client.get("/api/unesco/datasets", headers=HEADERS)
        assert response.status_code == 200
        data = response.json()
        assert "datasets" in data
        assert len(data["datasets"]) > 0

def test_get_unesco_records():
    """
    Test the /api/unesco/datasets/{dataset_id}/records endpoint with a mock.
    """
    dataset_id = "mock_id"
    with patch("api.unesco.get_records", return_value=get_mock_unesco_records(dataset_id)):
        response = client.get(f"/api/unesco/datasets/{dataset_id}/records", headers=HEADERS)
        assert response.status_code == 200
        data = response.json()
        assert "records" in data

def test_unesco_ml_predict():
    """
    Test the /api/unesco/ml/predict endpoint.
    """
    dataset_id = "mock_id"
    with patch("api.unesco.get_records", return_value=get_mock_unesco_records(dataset_id)):
        request_body = {"dataset_id": dataset_id}
        response = client.post("/api/unesco/ml/predict", json=request_body, headers=HEADERS)
        assert response.status_code == 200
        data = response.json()
        assert "mock_prediction" in data
