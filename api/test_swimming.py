from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)
API_KEY = "test-api-key"

def test_get_swimming_ai_action():
    response = client.post(
        "/api/swimming/ai/action",
        headers={"X-API-Key": API_KEY},
        json={"game_state": "swimming", "stroke_type": "freestyle"}
    )
    assert response.status_code == 200
    assert "AI Swimming Tip" in response.json()["action"]
    assert "freestyle" in response.json()["action"]

def test_swimming_reward():
    response = client.post(
        "/api/swimming/reward",
        headers={"X-API-Key": API_KEY},
        json={
            "owner_address": "0x1234567890123456789012345678901234567890",
            "metadata_uri": "https://games-universe.com/rewards/swimming_master.json"
        }
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "token_id" in response.json()

def test_get_swimming_nft_details():
    # First mint a reward to ensure it exists
    mint_response = client.post(
        "/api/swimming/reward",
        headers={"X-API-Key": API_KEY},
        json={
            "owner_address": "0x1234567890123456789012345678901234567890",
            "metadata_uri": "https://games-universe.com/rewards/swimming_master.json"
        }
    )
    token_id = mint_response.json()["token_id"]

    response = client.get(
        f"/api/swimming/nft/{token_id}",
        headers={"X-API-Key": API_KEY}
    )
    assert response.status_code == 200
    assert response.json()["owner"] == "0x1234567890123456789012345678901234567890"
