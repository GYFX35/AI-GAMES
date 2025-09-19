import json

import os

# Build the path relative to the current file
dir_path = os.path.dirname(os.path.realpath(__file__))
games_path = os.path.join(dir_path, "..", "frontend", "data", "minecraft_games.json")

def get_all_games():
    """
    Get a list of all Minecraft games from the JSON data file.
    """
    with open(games_path, "r") as f:
        return json.load(f)
