from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_shovel_master_ai_action():
    response = client.post(
        "/api/shovel_master/ai/action",
        headers={"X-API-Key": "test-api-key"},
        json={"game_state": "shovel_ready"}
    )
    assert response.status_code == 200
    assert "Action:" in response.json()["action"]
    assert "State: Shoveling" in response.json()["action"]

def test_shovel_master_reward():
    response = client.post(
        "/api/shovel_master/reward",
        headers={"X-API-Key": "test-api-key"},
        json={
            "owner_address": "0x123",
            "metadata_uri": "https://games-universe.com/rewards/shovel_master_gold.json"
        }
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["owner"] == "0x123"

def test_get_shovel_master_nft_details():
    # First mint a reward
    mint_response = client.post(
        "/api/shovel_master/reward",
        headers={"X-API-Key": "test-api-key"},
        json={
            "owner_address": "0x456",
            "metadata_uri": "https://games-universe.com/rewards/shovel_master_test.json"
        }
    )
    token_id = mint_response.json()["token_id"]

    response = client.get(
        f"/api/shovel_master/nft/{token_id}",
        headers={"X-API-Key": "test-api-key"}
    )
    assert response.status_code == 200
    assert response.json()["owner"] == "0x456"
