import unittest
from fastapi.testclient import TestClient
from api.main import app

class TestEcommerce(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.api_key = "test-api-key"
        self.headers = {"X-API-Key": self.api_key}

    def test_get_alibaba_products_success(self):
        response = self.client.get("/api/ecommerce/alibaba", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(len(data) > 0)
        self.assertEqual(data[0]["id"], "ali_001")

    def test_get_amazon_products_success(self):
        response = self.client.get("/api/ecommerce/amazon", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(len(data) > 0)
        self.assertEqual(data[0]["id"], "amz_001")

    def test_get_shopline_products_success(self):
        response = self.client.get("/api/ecommerce/shopline", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(len(data) > 0)
        self.assertEqual(data[0]["id"], "shl_001")

    def test_get_shopify_products_success(self):
        response = self.client.get("/api/ecommerce/shopify", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(len(data) > 0)
        self.assertEqual(data[0]["id"], "shp_001")

    def test_get_ecommerce_no_api_key(self):
        for endpoint in ["alibaba", "amazon", "shopline", "shopify"]:
            response = self.client.get(f"/api/ecommerce/{endpoint}")
            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()["detail"], "Not authenticated")
