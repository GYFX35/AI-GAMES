from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)
API_KEY = "test-api-key"

def test_animal_running_ai_action():
    response = client.post(
        "/api/animal_running/ai/action",
        headers={"X-API-Key": API_KEY},
        json={"game_state": "running", "animal_type": "lion"}
    )
    assert response.status_code == 200
    assert "lion is running" in response.json()["action"]

def test_animal_running_ai_obstacle():
    response = client.post(
        "/api/animal_running/ai/action",
        headers={"X-API-Key": API_KEY},
        json={"game_state": "obstacle_ahead", "animal_type": "tiger"}
    )
    assert response.status_code == 200
    assert "tiger encountered an obstacle" in response.json()["action"]

def test_animal_running_reward():
    response = client.post(
        "/api/animal_running/reward",
        headers={"X-API-Key": API_KEY},
        json={
            "owner_address": "0x123",
            "metadata_uri": "https://example.com/reward.json"
        }
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["owner"] == "0x123"

def test_get_animal_running_nft_details():
    # First mint one
    mint_response = client.post(
        "/api/animal_running/reward",
        headers={"X-API-Key": API_KEY},
        json={
            "owner_address": "0x456",
            "metadata_uri": "https://example.com/reward2.json"
        }
    )
    token_id = mint_response.json()["token_id"]

    response = client.get(
        f"/api/animal_running/nft/{token_id}",
        headers={"X-API-Key": API_KEY}
    )
    assert response.status_code == 200
    assert response.json()["owner"] == "0x456"
