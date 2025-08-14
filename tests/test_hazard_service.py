import pytest
from pavepath.hazard_service import get_hazards_for_segment
from pavepath.hazard_service import score_segment

def test_get_hazards_for_segment_structure():
    start = (33.7, -117.2)
    end = (33.8, -117.3)
    hazards = get_hazards_for_segment(start, end)

    # Check that the result is a dictionary
    assert isinstance(hazards, dict)

    # Check that all expected hazard types are present
    expected_keys = ['weather', 'road_condition', 'traffic', 'crime', 'natural_disaster']
    assert all(key in hazards for key in expected_keys)

def test_get_hazards_for_segment_values():
    start = (33.7, -117.2)
    end = (33.8, -117.3)
    hazards = get_hazards_for_segment(start, end)

    # Check that all values are floats between 0 and 10
    for value in hazards.values():
        assert isinstance(value, float)
        assert 0.0 <= value <= 10.0
        
def test_score_segment_output():
    hazards = {
        'weather': 5.0,
        'road_condition': 7.0,
        'traffic': 3.0,
        'crime': 6.0,
        'natural_disaster': 2.0
    }
    score = score_segment(hazards)
    assert isinstance(score, float)
    assert 0.0 <= score <= 10.0
    print(f"✅ Score test passed. Composite score: {score}")
