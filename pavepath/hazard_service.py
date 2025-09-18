from hazard_sources.osm_loader import load_osm_hazards
from hazard_scoring import score_hazards
from hazard_rules import should_reroute

def analyze_route(route_geometry, surface_data=None):
    """
    Analyze route for hazards and decide if rerouting is needed.
    Args:
        route_geometry (list[dict]): Segments with metadata
        surface_data (dict, optional): Surface type per location
    Returns:
        tuple: (scored hazards, reroute flag)
    """
    hazards = load_osm_hazards(route_geometry)
    scored = score_hazards(hazards, surface_data)
    reroute_flag = should_reroute(scored)
    return scored, reroute_flag

