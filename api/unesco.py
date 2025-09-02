import requests

BASE_URL = "https://data.unesco.org/api/explore/v2.0"

import sys

def get_datasets():
    """
    Fetches a list of all datasets from the UNESCO API.
    """
    url = f"{BASE_URL}/catalog/datasets"
    print(f"Fetching data from URL: {url}", flush=True)
    response = requests.get(url)
    print(f"Response status code: {response.status_code}", flush=True)
    response.raise_for_status()
    return response.json()

def get_records(dataset_id: str):
    """
    Fetches records from a specific dataset from the UNESCO API.
    """
    url = f"{BASE_URL}/catalog/datasets/{dataset_id}/records"
    print(f"Fetching data from URL: {url}", flush=True)
    try:
        response = requests.get(url)
        print(f"Response status code: {response.status_code}", flush=True)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr, flush=True)
        raise
