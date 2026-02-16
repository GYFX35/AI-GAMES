from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)
API_KEY = "test-api-key"

def test_get_tree_planting_ai_action():
    response = client.post(
        "/api/tree_planting/ai/action",
        headers={"X-API-Key": API_KEY},
        json={"game_state": "choosing_tree", "area": "forest"}
    )
    assert response.status_code == 200
    assert "AI Tip" in response.json()["action"]
    assert "forest" in response.json()["action"]

def test_tree_planting_reward():
    response = client.post(
        "/api/tree_planting/reward",
        headers={"X-API-Key": API_KEY},
        json={
            "owner_address": "0x1234567890123456789012345678901234567890",
            "metadata_uri": "https://games-universe.com/rewards/tree_guardian.json"
        }
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "token_id" in response.json()

def test_get_tree_planting_nft_details():
    # First mint a reward to ensure it exists
    mint_response = client.post(
        "/api/tree_planting/reward",
        headers={"X-API-Key": API_KEY},
        json={
            "owner_address": "0x1234567890123456789012345678901234567890",
            "metadata_uri": "https://games-universe.com/rewards/tree_guardian.json"
        }
    )
    token_id = mint_response.json()["token_id"]

    response = client.get(
        f"/api/tree_planting/nft/{token_id}",
        headers={"X-API-Key": API_KEY}
    )
    assert response.status_code == 200
    assert response.json()["owner"] == "0x1234567890123456789012345678901234567890"
