from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_monetag_postback_success():
    """
    Test a successful Monetag postback with all parameters.
    """
    # These are example values that Monetag might send.
    params = {
        "ymid": "user123-session456",
        "sum": 0.05,
        "currency": "USD",
        "zone": 123456,
        "requestvar": "rewarded_ad_level_complete"
    }

    # Make a GET request to the postback endpoint.
    response = client.get("/api/monetag/postback", params=params)

    # Assert that the request was successful.
    assert response.status_code == 200

    # Assert that the response body contains the expected message.
    assert response.json() == {"status": "ok", "message": "Postback received"}

def test_monetag_postback_missing_params():
    """
    Test a Monetag postback with some parameters missing.
    The endpoint should still handle it gracefully.
    """
    params = {
        "ymid": "user789",
        "sum": 0.01
    }

    response = client.get("/api/monetag/postback", params=params)
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Postback received"}

def test_monetag_postback_no_params():
    """
    Test a Monetag postback with no parameters at all.
    """
    response = client.get("/api/monetag/postback")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Postback received"}

def test_monetag_postback_invalid_param_type():
    """
    Test a postback where a parameter has an incorrect data type.
    FastAPI and Pydantic should handle this by returning a 422 Unprocessable Entity error.
    """
    params = {
        "sum": "not-a-float"
    }

    response = client.get("/api/monetag/postback", params=params)
    assert response.status_code == 422 # Unprocessable Entity