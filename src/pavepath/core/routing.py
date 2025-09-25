# pavepath/core/routing.py

from pavepath.hazard_service import simulate_hazards_for_segment, score_segment
from pavepath.route_optimizer import compute_segment_cost, get_driving_segments

def optimize_route(locations, mode="safe"):
    if not locations or len(locations) < 2:
        return {"segments": [], "mode": mode}

    if mode == "driving" and len(locations) == 2:
        origin, destination = locations
        segments, directions = get_driving_segments(origin, destination)
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
            "directions": directions,
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
        "directions": [],
        "mode": mode
    }
