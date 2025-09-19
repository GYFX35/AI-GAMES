import unittest
from unittest import mock
import requests
from api import fifa

class TestFifa(unittest.TestCase):

    @mock.patch('api.fifa.requests.get')
    def test_get_world_cup_data_success(self, mock_get):
        """
        Test that get_world_cup_data returns data on a successful API call.
        """
        mock_response = mock.Mock()
        expected_data = {"competitions": [{"id": 2000, "name": "FIFA World Cup"}]}
        mock_response.json.return_value = expected_data
        mock_response.raise_for_status = mock.Mock()
        mock_get.return_value = mock_response

        data = fifa.get_world_cup_data()

        self.assertEqual(data, expected_data)
        mock_get.assert_called_once_with("https://api.football-data.org/v4/competitions/")

    @mock.patch('api.fifa.requests.get')
    def test_get_world_cup_data_failure(self, mock_get):
        """
        Test that get_world_cup_data returns None on a failed API call.
        """
        mock_get.side_effect = requests.exceptions.RequestException("API call failed")

        data = fifa.get_world_cup_data()

        self.assertIsNone(data)
        mock_get.assert_called_once_with("https://api.football-data.org/v4/competitions/")

if __name__ == '__main__':
    unittest.main()
