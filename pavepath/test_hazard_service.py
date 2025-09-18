from hazard_service import analyze_route

# Mock route geometry with minimal metadata
mock_route = [
    {"location": "A", "surface": "unpaved"},
    {"location": "B", "flood_risk": True},
    {"location": "C", "surface": "paved"}
]

# Optional surface context
surface_data = {
    "A": "gravel",
    "B": "asphalt",
    "C": "paved"
}

# Run analysis
scored_hazards, should_reroute = analyze_route(mock_route, surface_data)

# Output results
print("Scored Hazards:")
for hazard in scored_hazards:
    print(hazard)

print("\nShould Reroute:", should_reroute)
