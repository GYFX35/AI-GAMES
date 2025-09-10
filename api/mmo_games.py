import requests

def get_all_games():
    """
    Get a list of all MMO games from the MMOBomb API.
    """
    url = "https://www.mmobomb.com/api1/games"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching MMO games: {e}")
        return []
