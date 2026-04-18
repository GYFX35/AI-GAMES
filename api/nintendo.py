import json
import os
from fastapi import APIRouter, Depends
from api.auth import get_api_key

router = APIRouter()

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "frontend", "data")

@router.get("/games")
async def get_nintendo_games(api_key: str = Depends(get_api_key)):
    path = os.path.join(DATA_PATH, "nintendo_games.json")
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)
