import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env

GEOCODING_API = "https://api.opencagedata.com/geocode/v1/json"
API_KEY = os.getenv("OPENCAGE_API_KEY")  # Securely loaded

def geocode_location(location: str):
    params = {"q": location, "key": API_KEY, "limit": 1}
    response = requests.get(GEOCODING_API, params=params)
    data = response.json()
    if data["results"]:
        coords = data["results"][0]["geometry"]
        return coords["lat"], coords["lng"]
    return None, None
