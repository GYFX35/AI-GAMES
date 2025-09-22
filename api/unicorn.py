# Unicorn API (Fun Translations) integration
import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.funtranslations.com/translate/yoda.json"
API_KEY = os.getenv("FUN_TRANSLATIONS_API_KEY")

def translate_text(text: str):
    """
    Translate text to Yoda speak using the Fun Translations API.
    """
    if not API_KEY:
        # Mock the response if no API key is available
        return {"success": {"total": 1}, "contents": {"translated": f"Translated: {text}", "text": text, "translation": "yoda"}}

    headers = {
        "X-Funtranslations-Api-Secret": API_KEY,
    }
    params = {"text": text}

    response = requests.get(BASE_URL, headers=headers, params=params)
    response.raise_for_status()
    return response.json()
