import json
import os
from fastapi import APIRouter, Depends
from api.auth import get_api_key

router = APIRouter()

# Setup paths robustly
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR_LOCAL = os.path.join(CURRENT_DIR, "..", "frontend", "data")
DATA_DIR_APP = "/app/frontend/data"

def load_products_file(filename: str):
    """
    Helper function to load e-commerce products from JSON file with multiple fallback paths.
    """
    for data_dir in [DATA_DIR_APP, DATA_DIR_LOCAL]:
        filepath = os.path.join(data_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                return json.load(f)
    return []

@router.get("/alibaba")
async def get_alibaba_products(api_key: str = Depends(get_api_key)):
    """
    Get all Alibaba products.
    """
    return load_products_file("alibaba_products.json")

@router.get("/amazon")
async def get_amazon_products(api_key: str = Depends(get_api_key)):
    """
    Get all Amazon products.
    """
    return load_products_file("amazon_products.json")

@router.get("/shopline")
async def get_shopline_products(api_key: str = Depends(get_api_key)):
    """
    Get all Shopline products.
    """
    return load_products_file("shopline_products.json")

@router.get("/shopify")
async def get_shopify_products(api_key: str = Depends(get_api_key)):
    """
    Get all Shopify products.
    """
    return load_products_file("shopify_products.json")
