import os
import json
from fastapi import APIRouter, HTTPException, Depends, Security
from pydantic import BaseModel
from typing import List, Optional
from api.auth import get_api_key

router = APIRouter()

# Path to the data file
DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "frontend", "data", "marketplace_items.json")

class MarketplaceItem(BaseModel):
    id: Optional[int] = None
    name: str
    category: str
    price: int  # in cents or in-game currency
    description: str
    image: str

def load_items() -> List[dict]:
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Error loading items: {e}")
        return []

def save_items(items: List[dict]):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(items, f, indent=4)
    except Exception as e:
        print(f"Error saving items: {e}")

@router.get("/", response_model=List[MarketplaceItem])
async def list_marketplace_items():
    """
    List all items available in the marketplace.
    """
    return load_items()

@router.get("/{item_id}", response_model=MarketplaceItem)
async def get_marketplace_item(item_id: int):
    """
    Get details of a specific marketplace item.
    """
    items = load_items()
    for item in items:
        if item.get("id") == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@router.post("/", response_model=MarketplaceItem, dependencies=[Depends(get_api_key)])
async def create_marketplace_item(item: MarketplaceItem):
    """
    Add a new item to the marketplace.
    """
    items = load_items()
    if not item.id:
        item.id = max([i.get("id", 0) for i in items]) + 1 if items else 1

    if any(i.get("id") == item.id for i in items):
        raise HTTPException(status_code=409, detail="Item with this ID already exists")

    items.append(item.dict())
    save_items(items)
    return item

@router.delete("/{item_id}", status_code=204, dependencies=[Depends(get_api_key)])
async def delete_marketplace_item(item_id: int):
    """
    Remove an item from the marketplace.
    """
    items = load_items()
    new_items = [i for i in items if i.get("id") != item_id]
    if len(new_items) == len(items):
        raise HTTPException(status_code=404, detail="Item not found")

    save_items(new_items)
    return {"status": "success"}

@router.get("/offers/dynamic", response_model=List[MarketplaceItem])
async def get_dynamic_offers(user_segment: str = "new_player"):
    """
    Get personalized offers based on user segmentation.
    Simplified implementation of the monetization algorithm.
    """
    all_items = load_items()

    # Simple logic for demonstration
    if user_segment == "whale":
        # Whales get premium items
        return [i for i in all_items if i["price"] > 1000]
    elif user_segment == "grinder":
        # Grinders get useful tools
        return [i for i in all_items if i["category"] == "Tools"]
    else:
        # Others get a mix or just the cheapest
        return sorted(all_items, key=lambda x: x["price"])[:2]
