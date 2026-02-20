from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

API_KEY = "test-api-key"

def test_get_papaya_peeling_ai_action():
    response = client.post(
        "/api/papaya_peeling/ai/action",
        headers={"X-API-Key": API_KEY},
        json={"game_state": "peeling", "peeling_quality": 0.9}
    )
    assert response.status_code == 200
    assert "AI Tip" in response.json()["action"]

def test_papaya_peeling_reward():
    response = client.post(
        "/api/papaya_peeling/reward",
        headers={"X-API-Key": API_KEY},
        json={"owner_address": "0x123", "metadata_uri": "https://example.com/papaya.json"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_get_papaya_peeling_nft_details():
    # First mint one
    mint_response = client.post(
        "/api/papaya_peeling/reward",
        headers={"X-API-Key": API_KEY},
        json={"owner_address": "0x123", "metadata_uri": "https://example.com/papaya.json"}
    )
    token_id = mint_response.json()["token_id"]

    response = client.get(
        f"/api/papaya_peeling/nft/{token_id}",
        headers={"X-API-Key": API_KEY}
    )
    assert response.status_code == 200
    assert response.json()["owner"] == "0x123"
