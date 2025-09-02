import pytest
import requests

BASE_URL = "http://127.0.0.1:8000"
API_KEY = "test-api-key"
HEADERS = {"X-API-Key": API_KEY}

def get_first_dataset_id():
    """
    Helper function to get the ID of the first dataset from the API.
    """
    response = requests.get(f"{BASE_URL}/api/unesco/datasets", headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    return data["datasets"][0]["dataset"]["dataset_id"]

def test_get_unesco_datasets():
    """
    Test the /api/unesco/datasets endpoint.
    """
    response = requests.get(f"{BASE_URL}/api/unesco/datasets", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "datasets" in data
    assert len(data["datasets"]) > 0

def test_get_unesco_records():
    """
    Test the /api/unesco/datasets/{dataset_id}/records endpoint.
    """
    dataset_id = get_first_dataset_id()
    response = requests.get(f"{BASE_URL}/api/unesco/datasets/{dataset_id}/records", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "records" in data

def test_unesco_ml_predict():
    """
    Test the /api/unesco/ml/predict endpoint.
    """
    dataset_id = get_first_dataset_id()
    request_body = {"dataset_id": dataset_id}
    response = requests.post(f"{BASE_URL}/api/unesco/ml/predict", json=request_body, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "mock_prediction" in data
