import math

def haversine(coord1, coord2):
    """
    Calculates the great-circle distance between two points on Earth.
    Parameters:
        coord1, coord2: Tuples of (latitude, longitude)
    Returns:
        Distance in kilometers
    """
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    R = 6371  # Earth radius in kilometers
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2)**2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def optimize_route(locations):
    """
    Optimizes the order of locations using a greedy nearest-neighbor approach.
    Parameters:
        locations: List of (lat, lon) tuples
    Returns:
        Ordered list of locations representing the optimized route
    """
    if not locations or len(locations) < 2:
        return locations

    unvisited = locations[:]
    route = [unvisited.pop(0)]  # Start from the first location

    while unvisited:
        last = route[-1]
        next_loc = min(unvisited, key=lambda loc: haversine(last, loc))
        route.append(next_loc)
        unvisited.remove(next_loc)

    return route

# Example usage
if __name__ == "__main__":
    sample_locations = [
        (33.8121, -117.9190),  # Anaheim
        (34.0522, -118.2437),  # Los Angeles
        (33.7701, -118.1937),  # Long Beach
        (33.8358, -117.9143),  # Santa Ana
    ]

    optimized = optimize_route(sample_locations)
    print("Optimized Route:")
    for loc in optimized:
        print(f"{loc}")
