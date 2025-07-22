def check_for_dirt_road(route_segment, dirt_roads):
    """Returns True if any segment in route overlaps with dirt road list"""
    return any(segment in dirt_roads for segment in route_segment)

def generate_alert(route_segment, dirt_roads):
    """Returns alert message and action options"""
    if check_for_dirt_road(route_segment, dirt_roads):
        return {
            "message": "⚠️ Dirt road detected along your route.",
            "options": ["Proceed", "Reroute"]
        }
    return {"message": None}
