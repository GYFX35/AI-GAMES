import unittest
from unittest.mock import patch
import requests
import mmo_games

class TestMMOGames(unittest.TestCase):

    @patch('mmo_games.requests.get')
    def test_get_all_games(self, mock_get):
        # Mock the API response
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"id": 1, "title": "Test Game 1"},
            {"id": 2, "title": "Test Game 2"}
        ]
        mock_get.return_value = mock_response

        # Call the function
        games = mmo_games.get_all_games()

        # Assert the results
        self.assertEqual(len(games), 2)
        self.assertEqual(games[0]['title'], 'Test Game 1')

    @patch('mmo_games.requests.get')
    def test_get_all_games_api_error(self, mock_get):
        # Mock an API error
        mock_get.side_effect = requests.exceptions.RequestException("API is down")

        # Call the function
        games = mmo_games.get_all_games()

        # Assert the results
        self.assertEqual(games, [])

if __name__ == '__main__':
    unittest.main()
