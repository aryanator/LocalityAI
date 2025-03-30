import requests
import os

# Load API key from environment variable

#GEOCODE_API_KEY = "5acRBgJ6yO9HundfNEBt9EBYdS232PDiIjsvcMrc_k4"
# if not GEOCODE_API_KEY:
#     raise ValueError("HERE_API_KEY environment variable not set.")

def geocode_location(location):
    """
    Convert a location (e.g., city, zip code) into latitude and longitude.
    """
    GEOCODE_API_KEY = "5acRBgJ6yO9HundfNEBt9EBYdS232PDiIjsvcMrc_k4"
    url = "https://geocode.search.hereapi.com/v1/geocode"
    params = {
        "q": location,
        "apiKey": GEOCODE_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    if "items" in data and len(data["items"]) > 0:
        lat = data["items"][0]["position"]["lat"]
        lng = data["items"][0]["position"]["lng"]
        return lat, lng
    else:
        raise ValueError(f"Location '{location}' not found.")