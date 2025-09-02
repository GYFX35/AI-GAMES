import json
import os
from typing import List, Dict, Any

# Build the path relative to the current file
dir_path = os.path.dirname(os.path.realpath(__file__))
products_path = os.path.join(dir_path, "..", "data", "iap_products.json")

def get_all_products() -> List[Dict[str, Any]]:
    """
    Retrieve all in-app purchase products from the catalog.
    """
    with open(products_path, "r") as f:
        return json.load(f)

def verify_purchase(receipt_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Verify a purchase receipt with the appropriate app store.

    In a real application, this function would make a request to the
    Google Play Developer API or Apple's App Store server to verify the
    purchase. For this example, we'll just simulate a successful verification.
    """
    # In a real implementation, you would use a library like
    # google-auth-oauthlib and google-api-python-client to verify the purchase.

    # For now, we'll just return a mock response.
    return {
        "status": "success",
        "message": "Purchase verified successfully.",
        "product_id": receipt_data.get("productId"),
    }
