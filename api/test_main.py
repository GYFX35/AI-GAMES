import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import io
from main import app

class TestModelsGCS(unittest.TestCase):
    def setUp(self):
        self.gcs_patcher = patch('main.gcs')
        self.mock_gcs = self.gcs_patcher.start()
        self.client = TestClient(app)

    def tearDown(self):
        self.gcs_patcher.stop()

    def test_upload_model(self):
        """
        Test uploading a model to GCS.
        """
        self.mock_gcs.list_blobs.return_value = []
        self.mock_gcs.upload_blob.return_value = "http://fake.url/model.obj"
        file_content = b"This is a test model."
        file = ("model.obj", io.BytesIO(file_content), "application/octet-stream")
        response = self.client.post("/models", files={"file": file})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"filename": "model.obj", "public_url": "http://fake.url/model.obj"})
        self.mock_gcs.upload_blob.assert_called_once()

    def test_upload_model_already_exists(self):
        """
        Test uploading a model that already exists in GCS.
        """
        self.mock_gcs.list_blobs.return_value = ["model.obj"]
        file_content = b"This is a test model."
        file = ("model.obj", io.BytesIO(file_content), "application/octet-stream")
        response = self.client.post("/models", files={"file": file})
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json(), {"detail": "File with this name already exists."})

    def test_list_models(self):
        """
        Test listing models from GCS.
        """
        self.mock_gcs.list_blobs.return_value = ["model1.obj", "model2.obj"]
        response = self.client.get("/models")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), ["model1.obj", "model2.obj"])

    def test_download_model(self):
        """
        Test downloading a model from GCS.
        """
        self.mock_gcs.download_blob.return_value = b"model content"
        response = self.client.get("/models/model.obj")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"model content")
        self.mock_gcs.download_blob.assert_called_with("model.obj")

    def test_download_model_not_found(self):
        """
        Test downloading a model that does not exist in GCS.
        """
        from google.cloud.exceptions import NotFound
        self.mock_gcs.download_blob.side_effect = NotFound("Model not found")
        response = self.client.get("/models/nonexistent.obj")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Model not found."})

    def test_delete_model(self):
        """
        Test deleting a model from GCS.
        """
        response = self.client.delete("/models/model.obj")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Model 'model.obj' deleted successfully."})
        self.mock_gcs.delete_blob.assert_called_with("model.obj")

    def test_delete_model_not_found(self):
        """
        Test deleting a model that does not exist in GCS.
        """
        from google.cloud.exceptions import NotFound
        self.mock_gcs.delete_blob.side_effect = NotFound("Model not found")
        response = self.client.delete("/models/nonexistent.obj")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Model not found."})

class TestMain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.get_api_keys_patcher = patch('main.get_api_keys')
        cls.mock_get_api_keys = cls.get_api_keys_patcher.start()
        cls.mock_get_api_keys.return_value = {"test-key": "test-api-key"}

    @classmethod
    def tearDownClass(cls):
        cls.get_api_keys_patcher.stop()

    def setUp(self):
        self.client = TestClient(app)
        self.api_key = "test-api-key"
        self.headers = {"X-API-Key": self.api_key}

    def test_get_ai_action(self):
        """
        Test the /api/hockey/ai/action endpoint.
        """
        game_state = {"puck_owner": "player"}
        response = self.client.post("/api/hockey/ai/action", json=game_state, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("action", data)
        self.assertIn(data["action"], ["skate_back", "check_player", "block_shot"])

        game_state = {"puck_owner": "ai"}
        response = self.client.post("/api/hockey/ai/action", json=game_state, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("action", data)
        self.assertIn(data["action"], ["skate_forward", "pass_puck", "shoot_puck"])

    @patch('main.blockchain_manager.get_nft_details')
    def test_get_nft_details(self, mock_get_nft_details):
        """
        Test the /api/hockey/nft/{token_id} endpoint.
        """
        mock_get_nft_details.return_value = {"owner": "0x123", "uri": "https://example.com/nft.json"}
        token_id = 1
        response = self.client.get(f"/api/hockey/nft/{token_id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("owner", data)
        self.assertIn("uri", data)

        mock_get_nft_details.return_value = None
        token_id = 999
        response = self.client.get(f"/api/hockey/nft/{token_id}", headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_xcode_generate(self):
        """
        Test the /api/xcode/generate endpoint.
        """
        request_body = {"prompt": "network"}
        response = self.client.post("/api/xcode/generate", json=request_body, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertIn("code", response_json)
        self.assertIn("URLSession", response_json["code"])

        request_body = {"prompt": "unknown"}
        response = self.client.post("/api/xcode/generate", json=request_body, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertIn("code", response_json)
        self.assertIn("Hello, World!", response_json["code"])

    @patch('fb_business.send_server_event')
    def test_facebook_webhook(self, mock_send_event):
        """
        Test the /api/facebook/webhook endpoint.
        """
        user_data = {"name": "Test User", "email": "test@example.com"}
        response = self.client.post("/api/facebook/webhook", json=user_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "success", "message": "Event processed"})
        mock_send_event.assert_called_once_with(user_data)
