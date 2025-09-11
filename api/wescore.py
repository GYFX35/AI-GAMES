import requests
import json
import os

def get_wescore_credentials():
    """
    Reads the wescore API key and secret from the api_keys.json file.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    keys_path = os.path.join(dir_path, "api_keys.json")
    with open(keys_path, "r") as f:
        keys = json.load(f)
        return keys.get("wescore", {})

credentials = get_wescore_credentials()
API_KEY = credentials.get("api_key")
API_SECRET = credentials.get("api_secret")

BASE_URL = "https://live-score-api.com/api-client"

def get_live_scores():
    """
    Fetches live scores from the live-score-api.com.
    """
    if not API_KEY or not API_SECRET or API_KEY == "YOUR_WESCORE_API_KEY":
        return {"error": "API key and secret not set for WeScore."}

    url = f"{BASE_URL}/scores/live?key={API_KEY}&secret={API_SECRET}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching live scores: {e}")
        return None

def get_all_fixtures():
    """
    Fetches all fixtures from the live-score-api.com.
    """
    if not API_KEY or not API_SECRET or API_KEY == "YOUR_WESCORE_API_KEY":
        return {"error": "API key and secret not set for WeScore."}

    url = f"{BASE_URL}/fixtures/matches?key={API_KEY}&secret={API_SECRET}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching fixtures: {e}")
        return None
