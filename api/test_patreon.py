import unittest
from unittest.mock import patch, mock_open
from api import patreon
import json

class TestPatreon(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps([
        {"id": "1", "attributes": {"creation_name": "Campaign 1"}}
    ]))
    def test_get_campaigns_success(self, mock_file):
        campaigns = patreon.get_campaigns()
        self.assertEqual(len(campaigns), 1)
        self.assertEqual(campaigns[0]['attributes']['creation_name'], 'Campaign 1')

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_get_campaigns_file_not_found(self, mock_file):
        campaigns = patreon.get_campaigns()
        self.assertEqual(len(campaigns), 1)
        self.assertEqual(campaigns[0]['attributes']['creation_name'], 'My Awesome Project')

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps([
        {"id": "101", "attributes": {"amount_cents": 500}}
    ]))
    def test_get_patrons_success(self, mock_file):
        patrons = patreon.get_patrons("1")
        self.assertEqual(len(patrons), 1)
        self.assertEqual(patrons[0]['attributes']['amount_cents'], 500)

if __name__ == '__main__':
    unittest.main()
