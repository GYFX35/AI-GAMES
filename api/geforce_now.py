import json
import os
from typing import List, Dict, Any

# Build the path relative to the current file
dir_path = os.path.dirname(os.path.realpath(__file__))
games_path = os.path.join(dir_path, "..", "frontend", "data", "geforce_now_games.json")

def get_all_games() -> List[Dict[str, Any]]:
    """
    Retrieve all games from the GeForce Now store.
    """
    with open(games_path, "r") as f:
        return json.load(f)
