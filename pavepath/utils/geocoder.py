import requests

GEOCODING_API = "https://api.opencagedata.com/geocode/v1/json"
API_KEY = "your_api_key_here"

def geocode_location(location: str):
    params = {"q": location, "key": API_KEY, "limit": 1}
    response = requests.get(GEOCODING_API, params=params)
    data = response.json()
    if data["results"]:
        coords = data["results"][0]["geometry"]
        return coords["lat"], coords["lng"]
    return None, None
