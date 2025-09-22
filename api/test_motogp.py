import unittest
from unittest.mock import patch, mock_open
import json
from api import motogp

class TestMotoGP(unittest.TestCase):

    def test_get_all_games(self):
        # Mock the data that would be in the JSON file
        mock_data = json.dumps([
            {"name": "MotoGP 23", "description": "The official MotoGP game for the 2023 season.", "link": "https://motogp.com/en/game", "download_link": "https://store.steampowered.com/app/2165730/MotoGP23/"},
            {"name": "MotoGP 22", "description": "Relive the 2022 season with all the official riders and tracks.", "link": "https://motogp.com/en/game", "download_link": "https://store.steampowered.com/app/1710580/MotoGP22/"}
        ])

        # Use mock_open to simulate opening the file
        with patch('builtins.open', mock_open(read_data=mock_data)) as mock_file:
            games = motogp.get_all_games()
            self.assertEqual(len(games), 2)
            self.assertEqual(games[0]['name'], 'MotoGP 23')
            # Check that the file was opened with the correct path
            mock_file.assert_called_once_with("/app/frontend/data/motogp_games.json", "r")

    def test_get_all_games_file_not_found(self):
        # Simulate a FileNotFoundError
        with patch('builtins.open', side_effect=FileNotFoundError):
            with self.assertRaises(FileNotFoundError):
                motogp.get_all_games()

if __name__ == '__main__':
    unittest.main()
