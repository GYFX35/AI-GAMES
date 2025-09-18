import os
import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from api.main import app

class TestGCSIntegration(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        # Set a dummy GCS_BUCKET_NAME for testing
        os.environ["GCS_BUCKET_NAME"] = "test-bucket"

    @patch("api.gcs.get_storage_client")
    def test_upload_model(self, mock_get_storage_client):
        # Mock the GCS client and bucket
        mock_bucket = MagicMock()
        mock_get_storage_client.return_value.bucket.return_value = mock_bucket

        # Mock the blob and its exists method
        mock_blob = MagicMock()
        mock_blob.exists.return_value = False
        mock_bucket.blob.return_value = mock_blob

        # Create a dummy file for upload
        file_content = b"test file content"
        file_name = "test_model.obj"

        # Make the request to the upload endpoint
        response = self.client.post(
            "/models",
            files={"file": (file_name, file_content, "application/octet-stream")}
        )

        # Assert that the response is successful
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"filename": file_name, "content_type": "application/octet-stream"})

        # Assert that the GCS upload method was called
        mock_bucket.blob.assert_called_with(file_name)
        mock_blob.upload_from_file.assert_called_once()

    @patch("api.gcs.get_storage_client")
    def test_upload_model_already_exists(self, mock_get_storage_client):
        # Mock the GCS client and bucket
        mock_bucket = MagicMock()
        mock_get_storage_client.return_value.bucket.return_value = mock_bucket

        # Mock the blob and its exists method to return True
        mock_blob = MagicMock()
        mock_blob.exists.return_value = True
        mock_bucket.blob.return_value = mock_blob

        # Create a dummy file for upload
        file_content = b"test file content"
        file_name = "test_model.obj"

        # Make the request to the upload endpoint
        response = self.client.post(
            "/models",
            files={"file": (file_name, file_content, "application/octet-stream")}
        )

        # Assert that the response is a 409 conflict
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json(), {"detail": "File with this name already exists."})

    @patch("api.gcs.get_storage_client")
    def test_list_models(self, mock_get_storage_client):
        # Mock the GCS client and list_blobs method
        mock_blob1 = MagicMock()
        mock_blob1.name = "model1.obj"
        mock_blob2 = MagicMock()
        mock_blob2.name = "model2.obj"
        mock_get_storage_client.return_value.list_blobs.return_value = [mock_blob1, mock_blob2]

        # Make the request to the list endpoint
        response = self.client.get("/models")

        # Assert that the response is successful and contains the list of models
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), ["model1.obj", "model2.obj"])

    @patch("api.gcs.get_storage_client")
    def test_download_model(self, mock_get_storage_client):
        # Mock the GCS client and bucket
        mock_bucket = MagicMock()
        mock_get_storage_client.return_value.bucket.return_value = mock_bucket

        # Mock the blob and its exists and download_as_bytes methods
        mock_blob = MagicMock()
        mock_blob.exists.return_value = True
        mock_blob.download_as_bytes.return_value = b"file content"
        mock_bucket.blob.return_value = mock_blob

        # Make the request to the download endpoint
        response = self.client.get("/models/test_model.obj")

        # Assert that the response is successful and contains the file content
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"file content")

    @patch("api.gcs.get_storage_client")
    def test_download_model_not_found(self, mock_get_storage_client):
        # Mock the GCS client and bucket
        mock_bucket = MagicMock()
        mock_get_storage_client.return_value.bucket.return_value = mock_bucket

        # Mock the blob and its exists method to return False
        mock_blob = MagicMock()
        mock_blob.exists.return_value = False
        mock_bucket.blob.return_value = mock_blob

        # Make the request to the download endpoint
        response = self.client.get("/models/test_model.obj")

        # Assert that the response is a 404 not found
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Model not found."})

    @patch("api.gcs.get_storage_client")
    def test_delete_model(self, mock_get_storage_client):
        # Mock the GCS client and bucket
        mock_bucket = MagicMock()
        mock_get_storage_client.return_value.bucket.return_value = mock_bucket

        # Mock the blob and its exists method
        mock_blob = MagicMock()
        mock_blob.exists.return_value = True
        mock_bucket.blob.return_value = mock_blob

        # Make the request to the delete endpoint
        response = self.client.delete("/models/test_model.obj")

        # Assert that the response is successful
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Model 'test_model.obj' deleted successfully."})

        # Assert that the GCS delete method was called
        mock_blob.delete.assert_called_once()

    @patch("api.gcs.get_storage_client")
    def test_delete_model_not_found(self, mock_get_storage_client):
        # Mock the GCS client and bucket
        mock_bucket = MagicMock()
        mock_get_storage_client.return_value.bucket.return_value = mock_bucket

        # Mock the blob and its exists method to return False
        mock_blob = MagicMock()
        mock_blob.exists.return_value = False
        mock_bucket.blob.return_value = mock_blob

        # Make the request to the delete endpoint
        response = self.client.delete("/models/test_model.obj")

        # Assert that the response is a 404 not found
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Model not found."})

if __name__ == "__main__":
    unittest.main()
