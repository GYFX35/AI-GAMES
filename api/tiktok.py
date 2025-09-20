import os
import json
import requests

TIKTOK_API_BASE_URL = "https://open.tiktokapis.com/v2"

def get_tiktok_api_keys():
    """
    Get TikTok API keys from the api_keys.json file.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    keys_path = os.path.join(dir_path, "api_keys.json")
    try:
        with open(keys_path, "r") as f:
            keys = json.load(f)
            return keys.get("tiktok", {})
    except FileNotFoundError:
        return {}

def get_access_token(code: str):
    """
    Exchange an authorization code for an access token.
    """
    api_keys = get_tiktok_api_keys()
    client_key = api_keys.get("client_key")
    client_secret = api_keys.get("client_secret")

    if not client_key or not client_secret:
        raise ValueError("TikTok client_key and client_secret must be set in api_keys.json")

    url = f"{TIKTOK_API_BASE_URL}/oauth/token/"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "client_key": client_key,
        "client_secret": client_secret,
        "code": code,
        "grant_type": "authorization_code"
    }
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()

def get_user_info(access_token: str):
    """
    Get user information from the TikTok API.
    """
    url = f"{TIKTOK_API_BASE_URL}/user/info/?fields=open_id,union_id,avatar_url,display_name"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_video_list(access_token: str, max_count: int = 20):
    """
    Get a list of videos from the TikTok API.
    """
    url = f"{TIKTOK_API_BASE_URL}/video/list/?fields=id,title,video_description,duration,cover_image_url,embed_link"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "max_count": max_count
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()
