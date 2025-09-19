import json

def get_all_games():
    """
    Get a list of all MotoGP games.

    For now, this returns mock data. In the future, this could be updated
    to fetch data from the Sportradar API.
    """
    with open("/app/frontend/data/motogp_games.json", "r") as f:
        return json.load(f)
