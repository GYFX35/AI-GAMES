import os
import requests
from typing import List, Dict, Any

# It's recommended to store the API key in an environment variable or a config file.
# For this example, we'll use a placeholder.
STEAM_API_KEY = os.environ.get("STEAM_API_KEY", "YOUR_STEAM_API_KEY")
STEAM_API_BASE_URL = "https://api.steampowered.com"

def get_all_games() -> List[Dict[str, Any]]:
    """
    Retrieve a list of all games from the Steam Web API.
    """
    url = f"{STEAM_API_BASE_URL}/ISteamApps/GetAppList/v2/"
    params = {"key": STEAM_API_KEY}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        return data.get("applist", {}).get("apps", [])
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []
