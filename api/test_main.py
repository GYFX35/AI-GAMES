import pytest
import requests
import os

BASE_URL = "http://127.0.0.1:8000"
API_KEY = "test-api-key"
HEADERS = {"X-API-Key": API_KEY}

def test_get_ai_action():
    """
    Test the /api/hockey/ai/action endpoint.
    """
    game_state = {"puck_owner": "player"}
    response = requests.post(f"{BASE_URL}/api/hockey/ai/action", json=game_state, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "action" in data
    assert data["action"] in ["skate_back", "check_player", "block_shot"]

    game_state = {"puck_owner": "ai"}
    response = requests.post(f"{BASE_URL}/api/hockey/ai/action", json=game_state, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "action" in data
    assert data["action"] in ["skate_forward", "pass_puck", "shoot_puck"]

def test_get_nft_details():
    """
    Test the /api/hockey/nft/{token_id} endpoint.
    """
    # Test with a valid token ID
    token_id = 1
    response = requests.get(f"{BASE_URL}/api/hockey/nft/{token_id}", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "owner" in data
    assert "uri" in data

    # Test with an invalid token ID
    token_id = 999
    response = requests.get(f"{BASE_URL}/api/hockey/nft/{token_id}", headers=HEADERS)
    assert response.status_code == 404

def test_track_games_endpoint():
    """
    Test the /api/games/track endpoint.
    """
    response = requests.post(f"{BASE_URL}/api/games/track", headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["message"] == "Game tracking initiated successfully."

    # Verify that the games.json file was created
    script_dir = os.path.dirname(__file__)
    data_dir = os.path.join(script_dir, "..", "data")
    file_path = os.path.join(data_dir, "games.json")
    assert os.path.exists(file_path)
