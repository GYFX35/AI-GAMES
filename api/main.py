import os
import shutil
import json
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Security
from fastapi.security import APIKeyHeader
from fastapi.responses import FileResponse
from typing import List, Optional
from pydantic import BaseModel
from ai_engine import HockeyAI, PadelAI
from blockchain import BlockchainManager
from xcode import XCodeManager
import unesco
import unesco_ml
import palm_store
import tencent_games
import geforce_now
import steam
import playstation
import amazon_luna
import mmo_games
import who_api
import fb_business
import wescore
import kickstarter
import patreon

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    """
    Initialize the Facebook API on application startup.
    """
    fb_business.init_facebook_api()

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

class HockeyGameState(BaseModel):
    puck_owner: str # "player", "ai", or "none"

class PadelGameState(BaseModel):
    game_state: str # "player_serves", "ai_serves", "ball_in_play"

class XCodeRequest(BaseModel):
    prompt: str

class UNESCOMLRequest(BaseModel):
    dataset_id: str

class FacebookUser(BaseModel):
    name: str
    email: Optional[str] = None

# --- API Key Authentication ---

API_KEY_HEADER = APIKeyHeader(name="X-API-Key")

def get_api_keys():
    # Build the path relative to the current file
    dir_path = os.path.dirname(os.path.realpath(__file__))
    keys_path = os.path.join(dir_path, "api_keys.json")
    with open(keys_path, "r") as f:
        return json.load(f)

def get_api_key(api_key_header: str = Security(API_KEY_HEADER)):
    api_keys = get_api_keys()
    if api_key_header not in api_keys.values(): # Corrected to check values
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

# --- XCode Endpoints ---
xcode_manager = XCodeManager()

@app.post("/api/xcode/generate", dependencies=[Depends(get_api_key)])
async def xcode_generate(xcode_request: XCodeRequest):
    """
    Generate Xcode (Swift) code based on a prompt.
    """
    code = xcode_manager.generate_code(xcode_request.prompt)
    return {"code": code}

# --- UNESCO Endpoints ---

@app.get("/api/unesco/datasets", dependencies=[Depends(get_api_key)])
async def get_unesco_datasets():
    """
    Get a list of all datasets from the UNESCO API.
    """
    return unesco.get_datasets()

@app.get("/api/unesco/datasets/{dataset_id}/records", dependencies=[Depends(get_api_key)])
async def get_unesco_records(dataset_id: str):
    """
    Get records from a specific dataset from the UNESCO API.
    """
    return unesco.get_records(dataset_id)

@app.post("/api/unesco/ml/predict", dependencies=[Depends(get_api_key)])
async def unesco_ml_predict(request: UNESCOMLRequest):
    """
    Run a mock prediction on a UNESCO dataset.
    """
    return unesco_ml.predict(request.dataset_id)

# --- Palm Store Endpoints ---

@app.get("/api/palm/games", dependencies=[Depends(get_api_key)])
async def get_palm_store_games():
    """
    Get a list of all games from the Palm Store.
    """
    return palm_store.get_all_games()

@app.get("/api/palm/games/{game_id}", dependencies=[Depends(get_api_key)])
async def get_palm_store_game(game_id: int):
    """
    Get a single game from the Palm Store by its ID.
    """
    game = palm_store.get_game_by_id(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found in Palm Store.")
    return game

# --- Tencent Games Endpoints ---

@app.get("/api/tencent/games", dependencies=[Depends(get_api_key)])
async def get_tencent_games():
    """
    Get a list of all games from Tencent Games.
    """
    return tencent_games.get_all_games()

# --- GeForce Now Endpoints ---

@app.get("/api/geforce-now/games", dependencies=[Depends(get_api_key)])
async def get_geforce_now_games():
    """
    Get a list of all games available on GeForce Now.
    """
    return geforce_now.get_all_games()

# --- Steam Endpoints ---

@app.get("/api/steam/games", dependencies=[Depends(get_api_key)])
async def get_steam_games():
    """
    Get a list of all games from Steam.
    """
    return steam.get_all_games()

# --- PlayStation Endpoints ---

@app.get("/api/playstation/games", dependencies=[Depends(get_api_key)])
async def get_playstation_games():
    """
    Get a list of all games from the PlayStation Store.
    """
    return playstation.get_all_games()

# --- Amazon Luna Endpoints ---

@app.get("/api/amazon-luna/games", dependencies=[Depends(get_api_key)])
async def get_amazon_luna_games():
    """
    Get a list of all games from the Amazon Luna store.
    """
    return amazon_luna.get_all_games()

# --- MMO Games Endpoints ---

@app.get("/api/mmo_games", dependencies=[Depends(get_api_key)])
async def get_mmo_games():
    """
    Get a list of all MMO games.
    """
    return mmo_games.get_all_games()

# --- WHO Endpoints ---

@app.get("/api/who_data", dependencies=[Depends(get_api_key)])
async def get_who_data():
    """
    Get a list of all indicators from the WHO GHO OData API.
    """
    return who_api.get_indicators()

@app.get("/api/web3_games")
async def get_web3_games():
    """
    Get a list of all web3 games.
    """
    with open("/app/data/web3_games.json", "r") as f:
        return json.load(f)

@app.get("/api/coupons")
async def get_coupons():
    """
    Get a list of all coupons.
    """
    with open("/app/data/coupons.json", "r") as f:
        return json.load(f)

@app.get("/api/pronostics")
async def get_pronostics():
    """
    Get a list of all pronostics.
    """
    with open("/app/data/pronostics.json", "r") as f:
        return json.load(f)

# --- Facebook Integration Endpoints ---

@app.post("/api/facebook/webhook")
async def facebook_webhook(user: FacebookUser):
    """
    Receives user data from the frontend after a Facebook login
    and sends a server-side event to the Conversions API.
    """
    print(f"Received Facebook user data: {user.dict()}")
    fb_business.send_server_event(user.dict())
    return {"status": "success", "message": "Event processed"}

# --- Hockey Game Endpoints ---

hockey_ai = HockeyAI()
blockchain_manager = BlockchainManager()

@app.post("/api/hockey/ai/action", dependencies=[Depends(get_api_key)])
async def get_ai_action(game_state: HockeyGameState):
    """
    Get the next action from the hockey AI.
    """
    action = hockey_ai.decide_action(game_state.dict())
    return {"action": action}

@app.get("/api/hockey/nft/{token_id}", dependencies=[Depends(get_api_key)])
async def get_nft_details(token_id: int):
    """
    Get the details of a player's NFT.
    """
    details = blockchain_manager.get_nft_details(token_id)
    if not details:
        raise HTTPException(status_code=404, detail="NFT not found.")
    return details

# --- Padel Game Endpoints ---

padel_ai = PadelAI()

@app.post("/api/padel/ai/action", dependencies=[Depends(get_api_key)])
async def get_padel_ai_action(game_state: PadelGameState):
    """
    Get the next action from the padel AI.
    """
    action = padel_ai.decide_action(game_state.game_state)
    return {"action": action}

@app.get("/api/padel/nft/{token_id}", dependencies=[Depends(get_api_key)])
async def get_padel_nft_details(token_id: int):
    """
    Get the details of a player's NFT for the padel game.
    """
    details = blockchain_manager.get_nft_details(token_id)
    if not details:
        raise HTTPException(status_code=404, detail="NFT not found.")
    return details

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

# --- WeScore Endpoints ---

@app.get("/api/wescore/scores", dependencies=[Depends(get_api_key)])
async def get_wescore_scores():
    """
    Get live scores from the WeScore API.
    """
    return wescore.get_live_scores()

@app.get("/api/wescore/fixtures", dependencies=[Depends(get_api_key)])
async def get_wescore_fixtures():
    """
    Get all fixtures from the WeScore API.
    """
    return wescore.get_all_fixtures()

# --- Kickstarter Endpoints ---

@app.get("/api/kickstarter/projects", dependencies=[Depends(get_api_key)])
async def get_kickstarter_projects(q: str = ""):
    """
    Get a list of all projects from Kickstarter.
    """
    return kickstarter.get_projects(q)

# --- Patreon Endpoints ---

@app.get("/api/patreon/campaigns", dependencies=[Depends(get_api_key)])
async def get_patreon_campaigns():
    """
    Get a list of all campaigns from Patreon.
    """
    return patreon.get_campaigns()

@app.get("/api/patreon/campaigns/{campaign_id}/patrons", dependencies=[Depends(get_api_key)])
async def get_patreon_patrons(campaign_id: str):
    """
    Get a list of all patrons for a campaign from Patreon.
    """
    return patreon.get_patrons(campaign_id)
