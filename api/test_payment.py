import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

class TestPayment(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.api_key = "test-api-key"
        self.headers = {"X-API-Key": self.api_key}

    @patch('stripe.checkout.Session.create')
    def test_create_checkout_session(self, mock_stripe_create):
        """
        Test the /api/payment/create-checkout-session endpoint.
        """
        mock_stripe_create.return_value = MagicMock(id='cs_test_123')

        product_data = {
            "name": "Test Product",
            "price": 1000,
            "quantity": 1
        }

        response = self.client.post("/api/payment/create-checkout-session", json=product_data, headers=self.headers)

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["id"], "cs_test_123")
        mock_stripe_create.assert_called_once_with(
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Test Product',
                    },
                    'unit_amount': 1000,
                },
                'quantity': 1,
            }],
            mode='payment',
            automatic_payment_methods={
                'enabled': True,
            },
            success_url='http://localhost/success.html',
            cancel_url='http://localhost/cancel.html',
        )

    @patch('stripe.checkout.Session.create')
    def test_create_sponsorship_checkout_session(self, mock_stripe_create):
        """
        Test the /api/payment/create-sponsorship-checkout-session endpoint.
        """
        mock_stripe_create.return_value = MagicMock(id='cs_test_456')

        sponsorship_data = {
            "amount": 5000
        }

        response = self.client.post("/api/payment/create-sponsorship-checkout-session", json=sponsorship_data, headers=self.headers)

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["id"], "cs_test_456")
        mock_stripe_create.assert_called_once_with(
            line_items=[{
                'price_data': {
                    'currency': 'ngn',
                    'product_data': {
                        'name': 'Sponsorship',
                    },
                    'unit_amount': 5000,
                },
                'quantity': 1,
            }],
            mode='payment',
            automatic_payment_methods={
                'enabled': True,
            },
            success_url='http://localhost/success.html',
            cancel_url='http://localhost/cancel.html',
        )

if __name__ == '__main__':
    unittest.main()
