import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env

GEOCODING_API = "https://api.opencagedata.com/geocode/v1/json"
API_KEY = os.getenv("OPENCAGE_API_KEY")  # Securely loaded
#print("[DEBUG] Loaded API key:", API_KEY)
print("[DEBUG] API_KEY:", repr(API_KEY))



def geocode_location(location: str):
    params = {"q": location, "key": API_KEY, "limit": 1}
    response = requests.get(GEOCODING_API, params=params, timeout=10)

    # Diagnostic print
    print("[DEBUG] Geocoder status:", response.status_code)
    print("[DEBUG] Geocoder response:", response.text)

    if response.status_code != 200:
        return None, None

    data = response.json()
    if data.get("results"):
        coords = data["results"][0]["geometry"]
        return coords["lat"], coords["lng"]
    return None, None

