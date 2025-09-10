import requests

def get_indicators():
    """
    Get a list of all indicators from the WHO GHO OData API.
    """
    url = "https://ghoapi.azureedge.net/api/Indicator"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching WHO indicators: {e}")
        return []
