import json
import os
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from api.auth import get_api_key

router = APIRouter()

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "frontend", "data")

def load_data(filename):
    path = os.path.join(DATA_PATH, filename)
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)

@router.get("/games")
async def get_twitch_games(api_key: str = Depends(get_api_key)):
    return load_data("twitch_games.json")

@router.get("/streams")
async def get_twitch_streams(game_id: Optional[str] = None, api_key: str = Depends(get_api_key)):
    streams = load_data("twitch_streams.json")
    if game_id:
        return [s for s in streams if s.get("game_id") == game_id]
    return streams
