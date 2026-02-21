from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)
API_KEY = "test-api-key"

def test_animal_fighting_ai_action():
    response = client.post(
        "/api/animal_fighting/ai/action",
        headers={"X-API-Key": API_KEY},
        json={
            "game_state": "fighting",
            "player_animal": "lion",
            "opponent_animal": "tiger"
        }
    )
    assert response.status_code == 200
    assert "AI Combat Tip" in response.json()["action"]
    assert "against the tiger" in response.json()["action"]

def test_animal_fighting_ai_victory():
    response = client.post(
        "/api/animal_fighting/ai/action",
        headers={"X-API-Key": API_KEY},
        json={
            "game_state": "victory",
            "player_animal": "gorilla",
            "opponent_animal": "elephant"
        }
    )
    assert response.status_code == 200
    assert "defeated the elephant" in response.json()["action"]

def test_animal_fighting_reward():
    response = client.post(
        "/api/animal_fighting/reward",
        headers={"X-API-Key": API_KEY},
        json={
            "owner_address": "0xFight",
            "metadata_uri": "https://example.com/champion.json"
        }
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["owner"] == "0xFight"

def test_get_animal_fighting_nft_details():
    # First mint one
    mint_response = client.post(
        "/api/animal_fighting/reward",
        headers={"X-API-Key": API_KEY},
        json={
            "owner_address": "0xWinner",
            "metadata_uri": "https://example.com/winner.json"
        }
    )
    token_id = mint_response.json()["token_id"]

    response = client.get(
        f"/api/animal_fighting/nft/{token_id}",
        headers={"X-API-Key": API_KEY}
    )
    assert response.status_code == 200
    assert response.json()["owner"] == "0xWinner"
