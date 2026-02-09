import unittest
from fastapi.testclient import TestClient
from api.main import app

class TestInvestigation(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.api_key = "test-api-key"
        self.headers = {"X-API-Key": self.api_key}

    def test_get_investigation_ai_action(self):
        """
        Test the /api/investigation/ai/action endpoint.
        """
        states_and_actions = {
            "scene_entered": ["search_for_fingerprints", "take_photos", "collect_dna_sample"],
            "clue_found": ["run_ballistics", "cross_reference_database", "decrypt_files"],
            "suspect_spotted": ["pursue_suspect", "call_for_backup", "deploy_drone"],
            "threat_detected": ["establish_perimeter", "interview_witnesses", "check_surveillance"]
        }

        for state, expected_actions in states_and_actions.items():
            game_state = {"game_state": state}
            response = self.client.post("/api/investigation/ai/action", json=game_state, headers=self.headers)
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("action", data)
            self.assertIn(data["action"], expected_actions)

    def test_get_investigation_nft_details(self):
        """
        Test the /api/investigation/nft/{token_id} endpoint.
        """
        # Test with a valid token ID
        token_id = 1
        response = self.client.get(f"/api/investigation/nft/{token_id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("owner", data)
        self.assertIn("uri", data)

        # Test with an invalid token ID
        token_id = 999
        response = self.client.get(f"/api/investigation/nft/{token_id}", headers=self.headers)
        self.assertEqual(response.status_code, 404)
