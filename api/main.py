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

@app.get("/api/games/search", response_model=List[Game], dependencies=[Depends(get_api_key)])
async def search_games(q: str = ""):
    """
    Search for games by name or category.
    """
    with open("../data/games.json", "r") as f:
        games = json.load(f)

    if not q:
        return games

    q = q.lower()
    results = [
        game for game in games
        if q in game["name"].lower() or q in game["category"].lower()
    ]
    return results

def get_bot_response(user_input: str) -> str:
    """
    A simple rule-based chatbot logic.
    """
    lower_case_input = user_input.lower()

    if 'hello' in lower_case_input or 'hi' in lower_case_input:
        return 'Hello! How can I help you today?'
    elif 'games' in lower_case_input:
        return 'You can find all our games on the Games page. Is there a specific game you are looking for?'
    elif 'search' in lower_case_input:
        return 'You can search for games on the Games page. Just type in the name or category of the game you are looking for.'
    elif 'help' in lower_case_input:
        return 'I can help you with questions about our games, the platform, and more. What do you need help with?'
    elif 'how are you' in lower_case_input:
        return 'I am just a bot, but I am doing great! Thanks for asking.'
    else:
        return 'I am sorry, I do not understand. Can you please rephrase your question?'

@app.post("/api/ai/chat", dependencies=[Depends(get_api_key)])
async def ai_chat(chat_request: ChatRequest):
    """
    Get a response from the AI assistant.
    """
    response = get_bot_response(chat_request.message)
    return {"response": response}

# The 'uploads' directory is at the root of the project.
# The API is run from the 'api' directory.
# So we need to go one level up.
UPLOADS_DIR = "../uploads"

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
