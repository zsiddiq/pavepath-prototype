import requests

GEOCODING_API = "https://api.opencagedata.com/geocode/v1/json"

def geocode_location(location: str, api_key: str, debug: bool = False):
    if debug:
        masked = lambda k: (k[:4] + "..." + k[-4:]) if k and len(k) > 8 else ("set" if k else "None")
        print(f"[geocoder] key loaded: {masked(api_key)} | query: '{location}'")

    if not api_key:
        if debug:
            print("[geocoder] Missing OPENCAGE_API_KEY")
        return None, None

    try:
        response = requests.get(
            GEOCODING_API,
            params={"q": location, "key": api_key, "limit": 1},
            timeout=12,
        )
        if debug:
            print(f"[geocoder] status={response.status_code}")
            print(f"[geocoder] url={response.url}")
            print(f"[geocoder] raw response={response.text[:300]}")

        if response.status_code != 200:
            return None, None

        data = response.json()
        results = data.get("results", [])
        if not results:
            if debug:
                print("[geocoder] No results returned")
            return None, None

        geometry = results[0].get("geometry", {})
        lat, lng = geometry.get("lat"), geometry.get("lng")
        if lat is None or lng is None:
            if debug:
                print("[geocoder] Missing lat/lng in geometry")
            return None, None

        return float(lat), float(lng)

    except requests.Timeout:
        if debug:
            print("[geocoder] Request timed out")
        return None, None
    except Exception as e:
        if debug:
            print(f"[geocoder] Exception: {e}")
        return None, None

