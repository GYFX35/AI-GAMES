import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)
API_KEY = "test-api-key"

def test_get_carpenter_ai_action():
    response = client.post(
        "/api/carpenter/ai/action",
        headers={"X-API-Key": API_KEY},
        json={"game_state": "measuring", "material": "oak"}
    )
    assert response.status_code == 200
    assert "action" in response.json()
    assert "AI Carpenter Tip" in response.json()["action"]

def test_carpenter_reward():
    response = client.post(
        "/api/carpenter/reward",
        headers={"X-API-Key": API_KEY},
        json={"owner_address": "0x123", "metadata_uri": "https://example.com/carpenter.json"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "token_id" in response.json()

def test_get_carpenter_nft_details():
    # First mint one
    mint_response = client.post(
        "/api/carpenter/reward",
        headers={"X-API-Key": API_KEY},
        json={"owner_address": "0x123", "metadata_uri": "https://example.com/carpenter.json"}
    )
    token_id = mint_response.json()["token_id"]

    response = client.get(
        f"/api/carpenter/nft/{token_id}",
        headers={"X-API-Key": API_KEY}
    )
    assert response.status_code == 200
    assert response.json()["owner"] == "0x123"
