import random
from typing import Tuple, Dict

def get_hazards_for_segment(start: Tuple[float, float], end: Tuple[float, float]) -> Dict[str, float]:
    """
    Simulates hazard data for a route segment.
    Returns a dictionary of hazard types and severity scores (0–10).
    """
    hazard_types = ['weather', 'road_condition', 'traffic', 'crime', 'natural_disaster']
    hazards = {hazard: round(random.uniform(0, 10), 2) for hazard in hazard_types}
    return hazards
