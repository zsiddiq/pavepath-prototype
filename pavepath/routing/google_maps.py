import googlemaps

def fetch_route(start, end, api_key):
    gmaps = googlemaps.Client(key=api_key)
    route = gmaps.directions(start, end, mode="driving")
    return route[0]['legs'][0]['steps']
