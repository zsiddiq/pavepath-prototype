import pytest
from pavepath.route_optimizer import haversine, optimize_route

def test_haversine_distance():
    d = haversine((0, 0), (0, 0))
    assert abs(d) < 1e-6

def test_optimize_route_runs():
    points = [(0, 0), (1, 1)]
    route = optimize_route(points)
    assert route is not None
