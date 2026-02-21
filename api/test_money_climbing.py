import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)
API_KEY = "test-api-key"

def test_money_climbing_ai_action():
    response = client.post(
        "/api/money_climbing/ai/action",
        headers={"X-API-Key": API_KEY},
        json={"game_state": "climbing", "height": 10.0, "money_collected": 50}
    )
    assert response.status_code == 200
    assert "action" in response.json()
    assert "AI Climbing Tip" in response.json()["action"]

def test_money_climbing_reward():
    response = client.post(
        "/api/money_climbing/reward",
        headers={"X-API-Key": API_KEY},
        json={
            "owner_address": "0x123",
            "metadata_uri": "https://example.com/money_climbing/nft.json"
        }
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "token_id" in response.json()

def test_money_climbing_nft_details():
    # First mint one
    mint_response = client.post(
        "/api/money_climbing/reward",
        headers={"X-API-Key": API_KEY},
        json={
            "owner_address": "0x123",
            "metadata_uri": "https://example.com/money_climbing/nft.json"
        }
    )
    token_id = mint_response.json()["token_id"]

    response = client.get(
        f"/api/money_climbing/nft/{token_id}",
        headers={"X-API-Key": API_KEY}
    )
    assert response.status_code == 200
    assert response.json()["owner"] == "0x123"
