import json
import os

def get_junglee_games():
    """
    Reads the list of Junglee games from the JSON file.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, '..', 'frontend', 'data', 'junglee_games.json')
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
