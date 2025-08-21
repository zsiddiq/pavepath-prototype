def annotate_route_with_hazards(steps, hazard_scores):
    for i, step in enumerate(steps):
        hazard = hazard_scores.get(f"segment_{i:03}", 0)
        step['hazard_score'] = hazard
    return steps
