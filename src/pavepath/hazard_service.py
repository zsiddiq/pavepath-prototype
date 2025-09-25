def analyze_route(route):
    segments = route.get("segments") if isinstance(route, dict) else route
    hazards = load_osm_hazards(segments)
    return {"hazards": hazards}

def load_osm_hazards(route_geometry):
    hazards = []
    for segment in route_geometry:
        if segment.get("surface") == "unpaved":
            hazards.append({"location": segment["location"], "type": "unpaved", "severity": 2, "score": 2})
        if segment.get("flood_risk"):
            hazards.append({"location": segment["location"], "type": "flood", "severity": 5, "score": 5})
    return hazards
