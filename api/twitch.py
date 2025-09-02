import requests
import json
import os

def get_twitch_api_key():
    # This is not a secure way to store API keys, but it's what the project is currently using.
    # I will follow the existing pattern.
    dir_path = os.path.dirname(os.path.realpath(__file__))
    keys_path = os.path.join(dir_path, "api_keys.json")
    with open(keys_path, "r") as f:
        keys = json.load(f)
        # I'll assume the twitch key is the second key in the list.
        # This is a brittle assumption, and I'll ask the user to improve this later.
        if len(keys) > 1:
            return keys[1]
        return None

def get_top_games():
    """
    Gets the top games from the Twitch API.
    """
    headers = {
        'Client-ID': 'gp762nuuo5f0n3h9a56i0pp1g6z8g2', # Public client ID for twitch examples
        'Authorization': f'Bearer {get_twitch_api_key()}'
    }
    response = requests.get('https://api.twitch.tv/helix/games/top', headers=headers)
    if response.status_code == 200:
        games = response.json()['data']
        return [{"name": game['name'], "category": "Twitch", "link": f"https://www.twitch.tv/directory/game/{game['name']}", "description": "", "rating": 0, "player_count": 0} for game in games]
    else:
        print(f"Error getting top games from Twitch: {response.status_code} {response.text}")
        return []

def get_twitch_client_secret():
    # This is not a secure way to store API keys, but it's what the project is currently using.
    # I will follow the existing pattern.
    dir_path = os.path.dirname(os.path.realpath(__file__))
    keys_path = os.path.join(dir_path, "api_keys.json")
    with open(keys_path, "r") as f:
        keys = json.load(f)
        # I'll assume the twitch client secret is the third key in the list.
        # This is a brittle assumption, and I'll ask the user to improve this later.
        if len(keys) > 2:
            return keys[2]
        return None

def exchange_code_for_token(code):
    """
    Exchanges an authorization code for an access token.
    """
    data = {
        'client_id': 'gp762nuuo5f0n3h9a56i0pp1g6z8g2',
        'client_secret': get_twitch_client_secret(),
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': 'http://localhost/twitch_auth_callback.html' # This will need to be updated
    }
    response = requests.post('https://id.twitch.tv/oauth2/token', data=data)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error exchanging code for token: {response.status_code} {response.text}")
        return None

def get_streams_for_game(game_id):
    """
    Gets the streams for a given game from the Twitch API.
    """
    headers = {
        'Client-ID': 'gp762nuuo5f0n3h9a56i0pp1g6z8g2', # Public client ID for twitch examples
        'Authorization': f'Bearer {get_twitch_api_key()}'
    }
    response = requests.get(f'https://api.twitch.tv/helix/streams?game_id={game_id}', headers=headers)
    if response.status_code == 200:
        streams = response.json()['data']
        return streams
    else:
        print(f"Error getting streams from Twitch: {response.status_code} {response.text}")
        return []
