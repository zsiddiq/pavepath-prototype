from pavepath.hazard_service import analyze_route

mock_route = [
    {"location": "A", "surface": "unpaved"},
    {"location": "B", "flood_risk": True},
    {"location": "C", "surface": "paved"}
]

surface_data = {"A": "gravel", "B": "asphalt", "C": "paved"}

if __name__ == "__main__":
    scored, reroute = analyze_route(mock_route, surface_data)
    print("Scored Hazards:", scored)
    print("Should Reroute:", reroute)
