from route_optimizer import optimize_route

sample_locations = [
    (33.8121, -117.9190),  # Anaheim
    (34.0522, -118.2437),  # Los Angeles
    (33.7701, -118.1937),  # Long Beach
    (33.8358, -117.9143),  # Santa Ana
]

optimized = optimize_route(sample_locations)

print("Optimized Route:")
for i, loc in enumerate(optimized, start=1):
    print(f"{i}. {loc}")
