import os
import json
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Security
from fastapi.security import APIKeyHeader
from fastapi.responses import FileResponse, Response
from typing import List, Optional
from pydantic import BaseModel
from api.ai_engine import HockeyAI, PadelAI, InvestigativeAI, ShovelMasterAI, AnimalRunningAI, TreePlantingAI
from api.blockchain import BlockchainManager
from api.xcode import XCodeManager
from api import unesco
from api import unesco_ml
from api import palm_store
from api import tencent_games
from api import geforce_now
from api import steam
from api import playstation
from api import amazon_luna
from api import ubisoft
from api import rival
from api import mmo_games
from api import minecraft
from api import netflix_games
from api import redbull
from api import junglee_games
from api import who_api
from api import fb_business
from api import wescore
from api import kickstarter
from api import patreon
from api import tiktok
from api import fifa
from api import makeup
from api import unicorn
from api import payment
from api import gcs
from api import monetag
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(payment.router, prefix="/api/payment", tags=["payment"])
app.include_router(monetag.router, prefix="/api/monetag", tags=["monetag"])

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

class InvestigationGameState(BaseModel):
    game_state: str # "scene_entered", "clue_found", "suspect_spotted", "threat_detected"

class ShovelMasterGameState(BaseModel):
    game_state: str # "shovel_ready", "shovel_full", "truck_full", "idle"

class AnimalRunningGameState(BaseModel):
    game_state: str # "ready", "running", "obstacle_ahead", "finish_line_near"
    animal_type: str # "lion", "tiger", etc.

class TreePlantingGameState(BaseModel):
    game_state: str # "choosing_tree", "planting", "idle"
    area: str # "forest", "desert", "city"

class RewardRequest(BaseModel):
    owner_address: str
    metadata_uri: str

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

# --- Endpoints ---

def get_games():
    with open("/app/frontend/data/games.json", "r") as f:
        return json.load(f)

def save_games(games: List[dict]):
    with open("/app/frontend/data/games.json", "w") as f:
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
    return Response(status_code=204)

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

# --- Ubisoft Endpoints ---

@app.get("/api/ubisoft/games", dependencies=[Depends(get_api_key)])
async def get_ubisoft_games():
    """
    Get a list of all games from Ubisoft.
    """
    return ubisoft.get_all_games()


# --- Red Bull Endpoints ---

@app.get("/api/redbull/games", dependencies=[Depends(get_api_key)])
async def get_redbull_games():
    """
    Get a list of all games from Red Bull.
    """
    return redbull.get_all_games()

# --- Netflix Games Endpoints ---

@app.get("/api/netflix/games", dependencies=[Depends(get_api_key)])
async def get_netflix_games():
    """
    Get a list of all games from Netflix.
    """
    return netflix_games.get_netflix_games()


# --- Junglee Games Endpoints ---

@app.get("/api/junglee/games", dependencies=[Depends(get_api_key)])
async def get_junglee_games():
    """
    Get a list of all games from Junglee Games.
    """
    return junglee_games.get_junglee_games()

# --- Rival Endpoints ---

@app.get("/api/rival/games", dependencies=[Depends(get_api_key)])
async def get_rival_games():
    """
    Get a list of all games from Rival.
    """
    return rival.get_all_games()

# --- MMO Games Endpoints ---

@app.get("/api/mmo_games", dependencies=[Depends(get_api_key)])
async def get_mmo_games():
    """
    Get a list of all MMO games.
    """
    return mmo_games.get_all_games()

# --- Minecraft Endpoints ---

@app.get("/api/minecraft/games", dependencies=[Depends(get_api_key)])
async def get_minecraft_games():
    """
    Get a list of all games from Minecraft.
    """
    return minecraft.get_all_games()

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
    with open("/app/frontend/data/web3_games.json", "r") as f:
        return json.load(f)

@app.get("/api/coupons")
async def get_coupons():
    """
    Get a list of all coupons.
    """
    with open("/app/frontend/data/coupons.json", "r") as f:
        return json.load(f)

@app.get("/api/pronostics")
async def get_pronostics():
    """
    Get a list of all pronostics.
    """
    with open("/app/frontend/data/pronostics.json", "r") as f:
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

# --- Investigation Game Endpoints ---

investigative_ai = InvestigativeAI()

# --- Shovel Master Game Endpoints ---

shovel_master_ai = ShovelMasterAI()

# --- Animal Running Game Endpoints ---

animal_running_ai = AnimalRunningAI()

# --- Tree Planting Game Endpoints ---

tree_planting_ai = TreePlantingAI()

@app.post("/api/animal_running/ai/action", dependencies=[Depends(get_api_key)])
async def get_animal_running_ai_action(game_state: AnimalRunningGameState):
    """
    Get the next action from the Animal Running AI.
    """
    action = animal_running_ai.decide_action(game_state.game_state, game_state.animal_type)
    return {"action": action}

@app.post("/api/animal_running/reward", dependencies=[Depends(get_api_key)])
async def animal_running_reward(request: RewardRequest):
    """
    Reward the player with an NFT for winning the competition.
    """
    reward = blockchain_manager.mint_reward(request.owner_address, request.metadata_uri)
    return reward

@app.get("/api/animal_running/nft/{token_id}", dependencies=[Depends(get_api_key)])
async def get_animal_running_nft_details(token_id: int):
    """
    Get the details of a reward NFT for the animal running game.
    """
    details = blockchain_manager.get_nft_details(token_id)
    if not details:
        raise HTTPException(status_code=404, detail="NFT not found.")
    return details

@app.post("/api/tree_planting/ai/action", dependencies=[Depends(get_api_key)])
async def get_tree_planting_ai_action(game_state: TreePlantingGameState):
    """
    Get the next action from the Tree Planting AI.
    """
    action = tree_planting_ai.decide_action(game_state.game_state, game_state.area)
    return {"action": action}

@app.post("/api/tree_planting/reward", dependencies=[Depends(get_api_key)])
async def tree_planting_reward(request: RewardRequest):
    """
    Reward the player with an NFT for planting trees.
    """
    reward = blockchain_manager.mint_reward(request.owner_address, request.metadata_uri)
    return reward

@app.get("/api/tree_planting/nft/{token_id}", dependencies=[Depends(get_api_key)])
async def get_tree_planting_nft_details(token_id: int):
    """
    Get the details of a reward NFT for the tree planting game.
    """
    details = blockchain_manager.get_nft_details(token_id)
    if not details:
        raise HTTPException(status_code=404, detail="NFT not found.")
    return details

@app.post("/api/shovel_master/ai/action", dependencies=[Depends(get_api_key)])
async def get_shovel_master_ai_action(game_state: ShovelMasterGameState):
    """
    Get the next action from the Shovel Master AI.
    """
    action = shovel_master_ai.decide_action(game_state.game_state)
    return {"action": action}

@app.post("/api/shovel_master/reward", dependencies=[Depends(get_api_key)])
async def shovel_master_reward(request: RewardRequest):
    """
    Reward the player with an NFT for filling the truck.
    """
    reward = blockchain_manager.mint_reward(request.owner_address, request.metadata_uri)
    return reward

@app.get("/api/shovel_master/nft/{token_id}", dependencies=[Depends(get_api_key)])
async def get_shovel_master_nft_details(token_id: int):
    """
    Get the details of a reward NFT for the shovel master game.
    """
    details = blockchain_manager.get_nft_details(token_id)
    if not details:
        raise HTTPException(status_code=404, detail="NFT not found.")
    return details

@app.post("/api/investigation/ai/action", dependencies=[Depends(get_api_key)])
async def get_investigation_ai_action(game_state: InvestigationGameState):
    """
    Get the next action from the investigative AI.
    """
    action = investigative_ai.decide_action(game_state.game_state)
    return {"action": action}

@app.get("/api/investigation/nft/{token_id}", dependencies=[Depends(get_api_key)])
async def get_investigation_nft_details(token_id: int):
    """
    Get the details of a player's NFT for the investigation game.
    """
    details = blockchain_manager.get_nft_details(token_id)
    if not details:
        raise HTTPException(status_code=404, detail="NFT not found.")
    return details

@app.post("/models", status_code=201)
async def upload_model(file: UploadFile = File(...)):
    """
    Upload a 3D model file.
    """
    if gcs.file_exists(file.filename):
        raise HTTPException(status_code=409, detail="File with this name already exists.")

    try:
        gcs.upload_file(file)
    finally:
        file.file.close()

    return {"filename": file.filename, "content_type": file.content_type}

@app.get("/models", response_model=List[str])
async def list_models():
    """
    Get a list of all available 3D models.
    """
    return gcs.list_files()

@app.get("/models/{model_name}")
async def download_model(model_name: str):
    """
    Download a 3D model file.
    """
    if not gcs.file_exists(model_name):
        raise HTTPException(status_code=404, detail="Model not found.")

    content = gcs.download_file(model_name)
    return Response(content, media_type="application/octet-stream")

@app.delete("/models/{model_name}")
async def delete_model(model_name: str):
    """
    Delete a 3D model file.
    """
    if not gcs.file_exists(model_name):
        raise HTTPException(status_code=404, detail="Model not found.")

    gcs.delete_file(model_name)
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

# --- TikTok Endpoints ---

class TikTokTokenRequest(BaseModel):
    code: str

@app.post("/api/tiktok/token", dependencies=[Depends(get_api_key)])
async def get_tiktok_token(request: TikTokTokenRequest):
    """
    Exchange an authorization code for a TikTok access token.
    """
    try:
        return tiktok.get_access_token(request.code)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/tiktok/user", dependencies=[Depends(get_api_key)])
async def get_tiktok_user(access_token: str):
    """
    Get user information from the TikTok API.
    """
    try:
        return tiktok.get_user_info(access_token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/tiktok/videos", dependencies=[Depends(get_api_key)])
async def get_tiktok_videos(access_token: str, max_count: int = 20):
    """
    Get a list of videos from the TikTok API.
    """
    try:
        return tiktok.get_video_list(access_token, max_count)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- FIFA Endpoints ---

@app.get("/api/fifa/world_cup", dependencies=[Depends(get_api_key)])
async def get_fifa_world_cup_data():
    """
    Get World Cup qualification data from the FIFA API.
    """
    data = fifa.get_world_cup_data()
    if data is None:
        raise HTTPException(status_code=500, detail="Could not fetch data from FIFA API.")
    return data

# --- Makeup Endpoints ---

@app.get("/api/makeup/products", dependencies=[Depends(get_api_key)])
async def get_makeup_products(brand: str = None, product_type: str = None):
    """
    Get a list of makeup products, optionally filtered by brand or product type.
    """
    return makeup.get_products(brand=brand, product_type=product_type)

# --- Unicorn Endpoints ---

class UnicornRequest(BaseModel):
    text: str

@app.post("/api/unicorn/translate", dependencies=[Depends(get_api_key)])
async def translate_for_unicorn(request: UnicornRequest):
    """
    Translate text into a unicorn-friendly dialect.
    """
    return unicorn.translate_text(request.text)
