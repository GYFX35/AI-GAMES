import unittest
from unittest.mock import patch, mock_open
from api import kickstarter
import json

class TestKickstarter(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps([
        {"title": "Test Project 1", "blurb": "A test blurb", "link": "http://test.com/1"},
        {"title": "Another Project", "blurb": "Another blurb", "link": "http://test.com/2"}
    ]))
    def test_get_projects_success(self, mock_file):
        # Call the function with a query that matches one project
        projects = kickstarter.get_projects("test")
        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0]['title'], 'Test Project 1')

        # Call the function without a query
        projects = kickstarter.get_projects("")
        self.assertEqual(len(projects), 2)

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_get_projects_file_not_found(self, mock_file):
        # Call the function with a query that matches one project in the default list
        projects = kickstarter.get_projects("awesome")
        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0]['title'], 'Awesome Game Project')

        # Test with a query that doesn't match anything in the default list
        projects = kickstarter.get_projects("non-existent")
        self.assertEqual(len(projects), 0)

        # Test without a query
        projects = kickstarter.get_projects("")
        self.assertEqual(len(projects), 2)

if __name__ == '__main__':
    unittest.main()
