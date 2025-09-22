# Makeup API integration
import requests

BASE_URL = "http://makeup-api.herokuapp.com/api/v1/products.json"

def get_products(brand: str = None, product_type: str = None):
    """
    Get makeup products from the Makeup API.
    """
    params = {}
    if brand:
        params["brand"] = brand
    if product_type:
        params["product_type"] = product_type

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()
