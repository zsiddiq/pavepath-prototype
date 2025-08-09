import pytest
from route_optimizer import haversine, optimize_route

def test_haversine_known_distance():
    # Los Angeles to San Francisco
    coord1 = (34.0522, -118.2437)
    coord2 = (37.7749, -122.4194)
    distance = haversine(coord1, coord2)
    assert 550 <= distance <= 650  # Approximate range in km

def test_optimize_route_returns_correct_length():
    locations = [
        (33.8121, -117.9190),  # Anaheim
        (34.0522, -118.2437),  # Los Angeles
        (33.7701, -118.1937),  # Long Beach
        (33.8358, -117.9143),  # Santa Ana
    ]
    optimized = optimize_route(locations)
    assert len(optimized) == len(locations)

def test_optimize_route_preserves_all_locations():
    locations = [
        (33.8121, -117.9190),
        (34.0522, -118.2437),
        (33.7701, -118.1937),
        (33.8358, -117.9143),
    ]
    optimized = optimize_route(locations)
    for loc in locations:
        assert loc in optimized

def test_optimize_route_empty_list():
    assert optimize_route([]) == []

def test_optimize_route_single_location():
    single = [(40.7128, -74.0060)]  # New York
    assert optimize_route(single) == single

def test_optimize_route_order_changes():
    locations = [
        (33.8121, -117.9190),
        (34.0522, -118.2437),
        (33.7701, -118.1937),
        (33.8358, -117.9143),
    ]
    optimized = optimize_route(locations)
    assert optimized != locations  # Should reorder unless already optimal
