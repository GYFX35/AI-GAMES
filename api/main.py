import os
import shutil
import json
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Security
from fastapi.security import APIKeyHeader
from fastapi.responses import FileResponse
from typing import List
from pydantic import BaseModel

app = FastAPI()

# --- Models ---

class Game(BaseModel):
    name: str
    category: str
    link: str
    description: str
    rating: float
    player_count: int

class ChatRequest(BaseModel):
    message: str

# --- API Key Authentication ---

API_KEY_HEADER = APIKeyHeader(name="X-API-Key")

def get_api_keys():
    with open("api_keys.json", "r") as f:
        return json.load(f)

def get_api_key(api_key_header: str = Security(API_KEY_HEADER)):
    api_keys = get_api_keys()
    if api_key_header not in api_keys:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API Key",
        )
    return api_key_header

# --- Endpoints ---

def get_games():
    with open("/app/data/games.json", "r") as f:
        return json.load(f)

def save_games(games: List[dict]):
    with open("/app/data/games.json", "w") as f:
        json.dump(games, f, indent=4)

@app.get("/api/games/search", response_model=List[Game], dependencies=[Depends(get_api_key)])
async def search_games(q: str = ""):
    """
    Search for games by name or category.
    """
    games = get_games()

    if not q:
        return games

    q = q.lower()
    results = [
        game for game in games
        if q in game["name"].lower() or q in game["category"].lower()
    ]
    return results

@app.post("/api/games", status_code=201, dependencies=[Depends(get_api_key)])
async def create_game(game: Game):
    """
    Add a new game to the platform.
    """
    games = get_games()
    if any(g["name"] == game.name for g in games):
        raise HTTPException(status_code=409, detail="Game with this name already exists.")

    games.append(game.dict())
    save_games(games)
    return game

@app.put("/api/games/{game_name}", response_model=Game, dependencies=[Depends(get_api_key)])
async def update_game(game_name: str, updated_game: Game):
    """
    Update an existing game.
    """
    games = get_games()
    for i, game in enumerate(games):
        if game["name"] == game_name:
            games[i] = updated_game.dict()
            save_games(games)
            return updated_game
    raise HTTPException(status_code=404, detail="Game not found.")

@app.delete("/api/games/{game_name}", status_code=204, dependencies=[Depends(get_api_key)])
async def delete_game(game_name: str):
    """
    Delete a game from the platform.
    """
    games = get_games()
    game_to_delete = None
    for game in games:
        if game["name"] == game_name:
            game_to_delete = game
            break

    if not game_to_delete:
        raise HTTPException(status_code=404, detail="Game not found.")

    games.remove(game_to_delete)
    save_games(games)

def mock_llm_call(prompt: str) -> str:
    """
    This is a mock function to simulate a call to a Large Language Model.
    In a real application, this would be replaced with a call to an external LLM service.
    """
    lower_case_prompt = prompt.lower()

    if 'game idea' in lower_case_prompt:
        return "How about a puzzle game where you play as a time-traveling detective who has to solve crimes by manipulating events in the past? Each level could be a different case with unique paradoxes to resolve."
    elif 'python code' in lower_case_prompt:
        return """Sure, here is a simple Python code snippet to get you started with our API:

import requests

API_KEY = "test-api-key"
BASE_URL = "http://localhost:8000"

def search_games(query):
    headers = {"X-API-Key": API_KEY}
    response = requests.get(f"{BASE_URL}/api/games/search?q={query}", headers=headers)
    return response.json()

print(search_games("AI"))
"""
    elif 'monetization' in lower_case_prompt:
        return "There are many ways to monetize a game. Some popular options include in-app purchases for cosmetic items, a subscription model for access to exclusive content, or a one-time purchase on an app store. The best model depends on your game's genre and target audience."
    else:
        return "I am a powerful AI assistant, ready to help you with your game development journey. Ask me for game ideas, code snippets, or anything else you need to bring your vision to life!"

def get_bot_response(user_input: str) -> str:
    """
    A simple rule-based chatbot logic that now calls a mock LLM.
    """
    return mock_llm_call(user_input)

@app.post("/api/ai/chat", dependencies=[Depends(get_api_key)])
async def ai_chat(chat_request: ChatRequest):
    """
    Get a response from the AI assistant.
    """
    response = get_bot_response(chat_request.message)
    return {"response": response}

# The 'uploads' directory is mapped to /app/uploads in the container
UPLOADS_DIR = "/app/uploads"

@app.post("/models", status_code=201)
async def upload_model(file: UploadFile = File(...)):
    """
    Upload a 3D model file.
    """
    if not os.path.exists(UPLOADS_DIR):
        os.makedirs(UPLOADS_DIR)

    file_path = os.path.join(UPLOADS_DIR, file.filename)

    if os.path.exists(file_path):
        raise HTTPException(status_code=409, detail="File with this name already exists.")

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()


    return {"filename": file.filename, "content_type": file.content_type}

@app.get("/models", response_model=List[str])
async def list_models():
    """
    Get a list of all available 3D models.
    """
    if not os.path.exists(UPLOADS_DIR):
        return []
    return os.listdir(UPLOADS_DIR)

@app.get("/models/{model_name}")
async def download_model(model_name: str):
    """
    Download a 3D model file.
    """
    file_path = os.path.join(UPLOADS_DIR, model_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Model not found.")
    return FileResponse(file_path)

@app.delete("/models/{model_name}")
async def delete_model(model_name: str):
    """
    Delete a 3D model file.
    """
    file_path = os.path.join(UPLOADS_DIR, model_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Model not found.")
    os.remove(file_path)
    return {"message": f"Model '{model_name}' deleted successfully."}
