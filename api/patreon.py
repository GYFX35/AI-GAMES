import json
import os

def get_campaigns():
    """
    Returns a list of mock Patreon campaigns.
    This is a mock implementation because API keys were not available.
    """
    return _get_mock_data("patreon_campaigns.json", [
        {
            "id": "1",
            "type": "campaign",
            "attributes": {
                "creation_name": "My Awesome Project",
                "patron_count": 123,
                "summary": "This is a summary of my awesome project."
            }
        }
    ])

def get_patrons(campaign_id: str):
    """
    Returns a list of mock patrons for a given campaign.
    This is a mock implementation.
    """
    # In a real implementation, you would filter patrons by campaign_id
    return _get_mock_data("patreon_patrons.json", [
        {
            "id": "101",
            "type": "pledge",
            "attributes": {
                "amount_cents": 500
            },
            "relationships": {
                "patron": {
                    "data": {
                        "id": "201",
                        "type": "user"
                    }
                }
            }
        }
    ])

def _get_mock_data(filename: str, default_data: list):
    """Helper to load mock data from a JSON file."""
    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.join(dir_path, "..", "data", filename)

    try:
        with open(data_path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default_data
