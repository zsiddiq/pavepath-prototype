import random
import math
from datetime import datetime, timezone
from typing import Tuple, Dict, List

# Tunable decay constant (controls how fast hazard scores fade over time)
DECAY_LAMBDA = 0.05

# Default hazard weights (can be adjusted dynamically)
HAZARD_WEIGHTS = {
    'weather': 0.2,
    'road_condition': 0.25,
    'traffic': 0.2,
    'crime': 0.2,
    'natural_disaster': 0.15
}

RISK_THRESHOLD = 6.0  # Threshold for flagging high-risk segments

# -------------------------------
# 🔹 Simulation Module
# -------------------------------

def simulate_hazards_for_segment(start: Tuple[float, float], end: Tuple[float, float]) -> Dict[str, Dict]:
    """
    Simulates hazard data for a route segment.
    Returns a dictionary of hazard types with severity and timestamp.
    """
    hazard_types = list(HAZARD_WEIGHTS.keys())
    hazards = {
        hazard: {
            'severity': round(random.uniform(0, 10), 2),
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        for hazard in hazard_types
    }
    return hazards

# -------------------------------
# 🔹 Scoring Module
# -------------------------------

def score_hazard(severity: float, timestamp_str: str) -> float:
    """
    Applies time decay to a hazard severity score.
    """
    timestamp = datetime.fromisoformat(timestamp_str)
    now = datetime.now(timezone.utc)
    age_hours = (now - timestamp).total_seconds() / 3600
    decay_factor = math.exp(-DECAY_LAMBDA * age_hours)
    return round(severity * decay_factor, 2)

def score_segment(hazards: Dict[str, Dict]) -> float:
    """
    Computes a composite hazard score from individual hazard types.
    Applies time decay and weighted average.
    """
    score = 0.0
    for hazard_type, data in hazards.items():
        severity = data.get('severity', 0)
        timestamp = data.get('timestamp')
        weight = HAZARD_WEIGHTS.get(hazard_type, 0)
        decayed_score = score_hazard(severity, timestamp)
        score += decayed_score * weight
    return round(score, 2)

# -------------------------------
# 🔹 Route Analysis Module
# -------------------------------

def analyze_route(route_hazards: List[Dict[str, Dict]]) -> Dict:
    """
    Analyzes a route composed of multiple segments with hazard data.
    Returns scores per segment, average score, and highest-risk segment.
    """
    segment_scores = []
    for i, hazards in enumerate(route_hazards):
        score = score_segment(hazards)
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
