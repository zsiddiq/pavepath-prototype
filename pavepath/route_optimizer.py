import math
import openrouteservice
from pavepath.hazard_service import simulate_hazards_for_segment, score_segment

# Tunable weights for composite cost function
HAZARD_WEIGHT = 0.7
DISTANCE_WEIGHT = 0.3

# ORS API key (replace with your actual key)
ORS_API_KEY = "your-api-key-here"

def haversine(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 6371  # Earth radius in km

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2)**2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def compute_segment_cost(start, end, mode="safe"):
    hazards = simulate_hazards_for_segment(start, end)
    hazard_score = score_segment(hazards)
    distance_km = haversine(start, end)

    if mode == "safe":
        cost = hazard_score * HAZARD_WEIGHT + distance_km * DISTANCE_WEIGHT
    else:  # mode == "fast"
        cost = distance_km

    return round(cost, 2), hazard_score, distance_km

def get_driving_segments(origin, destination):
    client = openrouteservice.Client(key=ORS_API_KEY)
    response = client.directions(
        coordinates=[origin, destination],
        profile='driving-car',
        format='geojson'
    )
    geometry = response['features'][0]['geometry']['coordinates']
    segments = [
        {"from": tuple(geometry[i]), "to": tuple(geometry[i+1])}
        for i in range(len(geometry) - 1)
    ]
    return segments

def optimize_route(locations, mode="safe"):
    """
    Optimizes route using composite cost (hazard + distance).
    Supports 'safe', 'fast', and 'driving' modes.
    """
    if not locations or len(locations) < 2:
        return {"segments": [], "mode": mode}

    if mode == "driving" and len(locations) == 2:
        origin, destination = locations
        segments = get_driving_segments(origin, destination)
        segment_details = []
        for seg in segments:
            cost, hazard_score, distance_km = compute_segment_cost(seg["from"], seg["to"], mode="safe")
            seg.update({
                "hazard_score": hazard_score,
                "distance_km": round(distance_km, 2),
                "composite_cost": cost
            })
            segment_details.append(seg)
        return {
            "optimized_route": [origin, destination],
            "segments": segment_details,
            "mode": mode
        }

    # Default greedy logic for multi-stop routing
    unvisited = locations[:]
    route = [unvisited.pop(0)]
    segment_details = []

    while unvisited:
        last = route[-1]
        next_loc, best_cost, hazard_score, distance_km = min(
            [(loc, *compute_segment_cost(last, loc, mode)) for loc in unvisited],
            key=lambda x: x[1]
        )
        route.append(next_loc)
        unvisited.remove(next_loc)
        segment_details.append({
            "from": last,
            "to": next_loc,
            "hazard_score": hazard_score,
            "distance_km": round(distance_km, 2),
            "composite_cost": best_cost
        })

    return {
        "optimized_route": route,
        "segments": segment_details,
        "mode": mode
    }

# Example usage
if __name__ == "__main__":
    sample_locations = [
        (33.680984, -117.170700),  # Menifee
        (33.835293, -117.914505),  # Anaheim
    ]

    result = optimize_route(sample_locations, mode="driving")
    print("Optimized Driving Route:")
    for seg in result["segments"]:
        print(f"{seg['from']} → {seg['to']} | Hazard: {seg['hazard_score']} | Distance: {seg['distance_km']} km | Cost: {seg['composite_cost']}")

