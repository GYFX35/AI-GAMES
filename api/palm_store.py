import json
import os
from typing import List, Dict, Any

# Build the path relative to the current file
dir_path = os.path.dirname(os.path.realpath(__file__))
games_path = os.path.join(dir_path, "..", "frontend", "data", "palm_store_games.json")

def get_all_games() -> List[Dict[str, Any]]:
    """
    Retrieve all games from the Palm Store.
    """
    with open(games_path, "r") as f:
        return json.load(f)

def get_game_by_id(game_id: int) -> Dict[str, Any]:
    """
    Retrieve a single game from the Palm Store by its ID.
    """
    games = get_all_games()
    for game in games:
        if game["id"] == game_id:
            return game
    return None
