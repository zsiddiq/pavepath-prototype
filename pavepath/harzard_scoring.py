def score_hazards(hazards, surface_data=None):
    """
    Assign severity scores to hazards and normalize them.
    Args:
        hazards (list[dict]): Raw hazard dicts with keys: location, type, severity
        surface_data (dict, optional): Surface type per location
    Returns:
        list[dict]: Hazard dicts with added 'score' key
    """
    scored = []
    for hazard in hazards:
        loc = hazard.get("location")
        base_score = hazard.get("severity", 1)

        # Adjust score based on surface context
        if surface_data and loc in surface_data:
            surface = surface_data[loc]
            if surface == "gravel":
                base_score += 1
            elif surface == "paved":
                base_score -= 1

        scored.append({**hazard, "score": max(base_score, 1)})
    return scored
