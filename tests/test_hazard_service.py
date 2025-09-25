import pytest
from pavepath.hazard_service import analyze_route

def test_analyze_route_returns_expected_structure():
    dummy_route = [
        {"id": 1, "location": "A", "surface": "unpaved", "flood_risk": True}
    ]
    result = analyze_route(dummy_route)
    assert isinstance(result, dict)
    assert "hazards" in result
