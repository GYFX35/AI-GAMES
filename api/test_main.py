import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from .main import app

client = TestClient(app)

API_KEY = "test-api-key"
HEADERS = {"X-API-Key": API_KEY}

def test_get_ai_action():
    """
    Test the /api/hockey/ai/action endpoint.
    """
    game_state = {"puck_owner": "player"}
    response = client.post("/api/hockey/ai/action", json=game_state, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "action" in data
    assert data["action"] in ["skate_back", "check_player", "block_shot"]

    game_state = {"puck_owner": "ai"}
    response = client.post("/api/hockey/ai/action", json=game_state, headers=HEADERS)
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
    response = client.get(f"/api/hockey/nft/{token_id}", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "owner" in data
    assert "uri" in data

    # Test with an invalid token ID
    token_id = 999
    response = client.get(f"/api/hockey/nft/{token_id}", headers=HEADERS)
    assert response.status_code == 404


def test_xcode_generate():
    """
    Test the /api/xcode/generate endpoint.
    """
    # Test with a prompt that should trigger the "network" template
    request_body = {"prompt": "network"}
    response = client.post("/api/xcode/generate", json=request_body, headers=HEADERS)
    assert response.status_code == 200
    response_json = response.json()
    assert "code" in response_json
    assert "URLSession" in response_json["code"]

    # Test with a prompt that should trigger the "default" template
    request_body = {"prompt": "unknown"}
    response = client.post("/api/xcode/generate", json=request_body, headers=HEADERS)
    assert response.status_code == 200
    response_json = response.json()
    assert "code" in response_json
    assert "Hello, World!" in response_json["code"]


def test_facebook_webhook():
    """
    Test the /api/facebook/webhook endpoint.
    It should call the send_server_event function.
    """
    # Mock the send_server_event function to avoid real API calls
    with patch('api.facebook_business.send_server_event') as mock_send_event:
        user_data = {"name": "Test User", "email": "test@example.com"}

        # The webhook endpoint does not require an API key
        response = client.post("/api/facebook/webhook", json=user_data)

        assert response.status_code == 200
        assert response.json() == {"status": "success", "message": "Event processed"}

        # Verify that our mocked function was called once with the correct data
        mock_send_event.assert_called_once_with(user_data)
