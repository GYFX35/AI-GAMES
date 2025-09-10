import unittest
from unittest.mock import patch
import requests
import who_api

class TestWhoApi(unittest.TestCase):

    @patch('who_api.requests.get')
    def test_get_indicators(self, mock_get):
        # Mock the API response
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "value": [
                {"IndicatorCode": "TEST1", "IndicatorName": "Test Indicator 1"},
                {"IndicatorCode": "TEST2", "IndicatorName": "Test Indicator 2"}
            ]
        }
        mock_get.return_value = mock_response

        # Call the function
        indicators = who_api.get_indicators()

        # Assert the results
        self.assertEqual(len(indicators['value']), 2)
        self.assertEqual(indicators['value'][0]['IndicatorName'], 'Test Indicator 1')

    @patch('who_api.requests.get')
    def test_get_indicators_api_error(self, mock_get):
        # Mock an API error
        mock_get.side_effect = requests.exceptions.RequestException("API is down")

        # Call the function
        indicators = who_api.get_indicators()

        # Assert the results
        self.assertEqual(indicators, [])

if __name__ == '__main__':
    unittest.main()
