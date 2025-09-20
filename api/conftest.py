import pytest
import json
import os

@pytest.fixture(autouse=True)
def api_keys_fixture():
    """
    Creates a dummy api_keys.json file for testing.
    This fixture is automatically used by all tests.
    """
    api_keys = {
        "test-key": "test-api-key",
        "tiktok": {
            "client_key": "test_client_key",
            "client_secret": "test_client_secret"
        }
    }
    with open("api_keys.json", "w") as f:
        json.dump(api_keys, f)

    yield

    # Clean up the dummy api_keys.json file
    if os.path.exists("api_keys.json"):
        os.remove("api_keys.json")
