import requests

def get_world_cup_data():
    """
    Fetches World Cup qualification data from the football-data.org API.
    """
    url = "https://api.football-data.org/v4/competitions/"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None
