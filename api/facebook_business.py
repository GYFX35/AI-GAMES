import json
import time
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.serverside.user_data import UserData
from facebook_business.adobjects.serverside.event import Event
from facebook_business.adobjects.serverside.event_request import EventRequest
from facebook_business.adobjects.serverside.custom_data import CustomData

def init_facebook_api():
    """
    Initializes the Facebook Ads API with credentials from api_keys.json.
    """
    try:
        with open('api/api_keys.json') as f:
            keys = json.load(f)
        facebook_keys = keys.get('facebook', {})
        app_id = facebook_keys.get('app_id')
        app_secret = facebook_keys.get('app_secret')
        access_token = facebook_keys.get('access_token')

        # Check if keys are placeholders
        if not all([app_id, app_secret, access_token]) or 'YOUR_FACEBOOK' in app_id:
            print("Facebook API credentials not found or are placeholders in api_keys.json")
            return None

        FacebookAdsApi.init(app_id=app_id, app_secret=app_secret, access_token=access_token)
        print("Facebook API initialized successfully.")
        return True
    except FileNotFoundError:
        print("api_keys.json not found.")
        return None
    except Exception as e:
        print(f"An error occurred during Facebook API initialization: {e}")
        return None

def send_server_event(user_data: dict):
    """
    Sends a "CompleteRegistration" server-side event to the Facebook Conversions API.
    """
    print(f"Attempting to send 'CompleteRegistration' event for user: {user_data.get('email')}")

    # Get Pixel ID
    try:
        with open('api/api_keys.json') as f:
            keys = json.load(f)
        pixel_id = keys.get('facebook', {}).get('pixel_id')
        if not pixel_id or 'YOUR_FACEBOOK_PIXEL_ID' in pixel_id:
            print("Facebook Pixel ID not found or is a placeholder in api_keys.json. Aborting event send.")
            return
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading or parsing api_keys.json: {e}. Aborting event send.")
        return

    # Prepare user data from the input dictionary
    email = user_data.get('email')
    full_name = user_data.get('name', '').split(' ')
    first_name = full_name[0]
    last_name = full_name[-1] if len(full_name) > 1 else ''

    # The SDK handles hashing for you if you provide plain text.
    user_data_object = UserData(
        em=[email] if email else [],
        fn=[first_name] if first_name else [],
        ln=[last_name] if last_name else [],
    )

    # Prepare the "CompleteRegistration" event
    event = Event(
        event_name='CompleteRegistration',
        event_time=int(time.time()),
        user_data=user_data_object,
        action_source='website',
    )

    # Create the event request and execute it
    try:
        event_request = EventRequest(
            events=[event],
            pixel_id=pixel_id,
        )
        event_response = event_request.execute()
        print(f"Successfully sent 'CompleteRegistration' event to Facebook Conversions API.")
    except Exception as e:
        print(f"Failed to send event to Facebook Conversions API: {e}")
