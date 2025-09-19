import json
from typing import List, Dict, Any

def get_all_games() -> List[Dict[str, Any]]:
    """
    Retrieve a list of all games from the mock Rival data file.
    """
    with open("/app/frontend/data/rival_games.json", "r") as f:
        return json.load(f)
