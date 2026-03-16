import os
import json
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

API_KEY_HEADER = APIKeyHeader(name="X-API-Key")

def get_api_keys():
    # Build the path relative to the current file
    dir_path = os.path.dirname(os.path.realpath(__file__))
    keys_path = os.path.join(dir_path, "api_keys.json")
    try:
        with open(keys_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"test-key": "test-api-key"}

def get_api_key(api_key_header: str = Security(API_KEY_HEADER)):
    api_keys = get_api_keys()
    if api_key_header not in api_keys.values(): # Corrected to check values
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API Key",
        )
    return api_key_header
