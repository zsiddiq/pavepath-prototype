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
    
def score_segment(hazards: Dict[str, float]) -> float:
    """
    Computes a composite hazard score from individual hazard severities.
    Uses weighted average to reflect importance of each hazard type.
    """
    weights = {
        'weather': 0.2,
        'road_condition': 0.25,
        'traffic': 0.2,
        'crime': 0.2,
        'natural_disaster': 0.15
    }

    score = sum(hazards[h] * weights.get(h, 0) for h in hazards)
    return round(score, 2)
def analyze_route(route_hazards: list) -> dict:
    """
    Analyzes a route composed of multiple segments with hazard data.
    
    Args:
        route_hazards (list): A list of dictionaries, each representing hazard data for a segment.
    
    Returns:
        dict: Contains scores per segment, average score, and highest-risk segment info.
    """
    RISK_THRESHOLD = 6.0  # ← Add this at the top of the function

    segment_scores = []
    for i, hazards in enumerate(route_hazards):
        score = score_segment(hazards)
        
        # 🚨 Upgrade 1: Risk Alert
        if score > RISK_THRESHOLD:
            print(f"⚠️ Warning: Segment {i} has a high hazard score of {score}")
        
        segment_scores.append({
            'segment': i,
            'score': score,
            'hazards': hazards
        })

    average_score = round(sum(s['score'] for s in segment_scores) / len(segment_scores), 2)
    highest_risk = max(segment_scores, key=lambda s: s['score'])

    return {
        'segment_scores': segment_scores,
        'average_score': average_score,
        'highest_risk_segment': highest_risk
    }
