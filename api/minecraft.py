import json

def get_all_games():
    """
    Get a list of all Minecraft games from the JSON data file.
    """
    with open("frontend/data/minecraft_games.json", "r") as f:
        return json.load(f)
