def should_reroute(scored_hazards, threshold=4):
    """
    Decide whether to reroute based on hazard scores.
    Args:
        scored_hazards (list[dict]): Hazards with 'score' key
        threshold (int): Minimum score to trigger reroute
    Returns:
        bool: True if reroute is recommended
    """
    for hazard in scored_hazards:
        if hazard.get("score", 0) >= threshold:
            return True
    return False
