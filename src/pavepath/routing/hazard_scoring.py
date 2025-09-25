def generate_hazard_scores(route_steps):
    # Example logic — replace with your real diagnostic model
    scores = {}
    for i, step in enumerate(route_steps):
        scores[f"segment_{i:03}"] = round(1 - (step['distance']['value'] / 10000), 2)
    return scores
