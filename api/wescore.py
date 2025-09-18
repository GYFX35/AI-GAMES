import requests
import json
import os

BASE_URL = "https://live-score-api.com/api-client"

def get_wescore_credentials():
    """
    Reads the wescore API key and secret from the api_keys.json file.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    keys_path = os.path.join(dir_path, "api_keys.json")
    try:
        with open(keys_path, "r") as f:
            keys = json.load(f)
            return keys.get("wescore", {})
    except FileNotFoundError:
        return {}

def get_live_scores():
    """
    Fetches live scores from the live-score-api.com.
    """
    credentials = get_wescore_credentials()
    api_key = credentials.get("api_key")
    api_secret = credentials.get("api_secret")

    if not api_key or not api_secret or api_key == "YOUR_WESCORE_API_KEY":
        return {"error": "API key and secret not set for WeScore."}

    url = f"{BASE_URL}/scores/live?key={api_key}&secret={api_secret}"
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
    credentials = get_wescore_credentials()
    api_key = credentials.get("api_key")
    api_secret = credentials.get("api_secret")

    if not api_key or not api_secret or api_key == "YOUR_WESCORE_API_KEY":
        return {"error": "API key and secret not set for WeScore."}

    url = f"{BASE_URL}/fixtures/matches?key={api_key}&secret={api_secret}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching fixtures: {e}")
        return None
