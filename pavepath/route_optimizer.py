import math
from pavepath.hazard_service import simulate_hazards_for_segment, score_segment


# Tunable weights for composite cost function
HAZARD_WEIGHT = 0.7
DISTANCE_WEIGHT = 0.3

def haversine(coord1, coord2):
    """
    Calculates the great-circle distance between two points on Earth.
    Returns distance in kilometers.
    """
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
    """
    Computes composite cost of a segment using hazard score and distance.
    """
    hazards = simulate_hazards_for_segment(start, end)
    hazard_score = score_segment(hazards)
    distance_km = haversine(start, end)

    if mode == "safe":
        cost = hazard_score * HAZARD_WEIGHT + distance_km * DISTANCE_WEIGHT
    else:  # mode == "fast"
        cost = distance_km  # ignore hazard score

    return round(cost, 2), hazard_score, distance_km

def optimize_route(locations, mode="safe"):
    """
    Optimizes route using composite cost (hazard + distance).
    Greedy nearest-neighbor approach based on cost.
    """
    if not locations or len(locations) < 2:
        return locations

    unvisited = locations[:]
    route = [unvisited.pop(0)]  # Start from first location
    segment_details = []

    while unvisited:
        last = route[-1]
        next_loc, best_cost, hazard_score, distance_km = min(
            [(loc, *compute_segment_cost(last, loc, mode)) for loc in unvisited],
            key=lambda x: x[1]  # sort by cost
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
        (33.8121, -117.9190),  # Anaheim
        (34.0522, -118.2437),  # Los Angeles
        (33.7701, -118.1937),  # Long Beach
        (33.8358, -117.9143),  # Santa Ana
    ]

    result = optimize_route(sample_locations, mode="safe")
    print("Optimized Hazard-Aware Route:")
    for seg in result["segments"]:
        print(f"{seg['from']} → {seg['to']} | Hazard: {seg['hazard_score']} | Distance: {seg['distance_km']} km | Cost: {seg['composite_cost']}")
