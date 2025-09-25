def load_osm_hazards(route_geometry):
    """
    Extract hazard-related tags from OSM-like data along the route.
    Args:
        route_geometry (list[dict]): Route segments with minimal metadata.
            Example segment: {"location": "A", "surface": "unpaved", "flood_risk": True}
    Returns:
        list[dict]: Hazard dicts with keys: location, type, severity
    """
    hazards = []
    for segment in route_geometry:
        loc = segment.get("location")
        surface = segment.get("surface")
        if surface in {"unpaved", "gravel"}:
            hazards.append({"location": loc, "type": "unpaved", "severity": 2})
        if segment.get("flood_risk"):
            hazards.append({"location": loc, "type": "flood", "severity": 5})
    return hazards
