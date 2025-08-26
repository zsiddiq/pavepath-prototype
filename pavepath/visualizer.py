import matplotlib.pyplot as plt
import folium

def visualize_route_scores(segment_scores: list, save=False):
    """
    Displays a bar chart of hazard scores per segment.
    Optionally saves the chart as a PNG.
    """
    segments = [s['segment'] for s in segment_scores]
    scores = [s['score'] for s in segment_scores]

    plt.figure(figsize=(10, 5))
    bars = plt.bar(segments, scores, color=['red' if s > 6 else 'green' for s in scores])
    plt.axhline(y=6, color='orange', linestyle='--', label='Risk Threshold')
    plt.xlabel('Segment')
    plt.ylabel('Hazard Score')
    plt.title('Route Hazard Analysis')
    plt.legend()
    plt.tight_layout()

    if save:
        plt.savefig("route_hazard_chart.png")
    else:
        plt.show()

def render_route_map(route_data: dict):
    """
    Renders a Folium map with route and hazard overlays.
    Input: route_data dict with 'optimized_route' and 'segments'
    """
    route = route_data.get("optimized_route", [])
    segments = route_data.get("segments", [])

    if not route or not segments:
        raise ValueError("Missing route or segment data")

    m = folium.Map(location=route[0], zoom_start=12)
    folium.PolyLine(route, color="blue", weight=4, opacity=0.6).add_to(m)

    for seg in segments:
        midpoint = (
            (seg["from"][0] + seg["to"][0]) / 2,
            (seg["from"][1] + seg["to"][1]) / 2
        )
        score = seg["hazard_score"]
        color = "green" if score < 2 else "orange" if score < 4 else "red"
        popup = (
            f"<b>Hazard Score:</b> {score}<br>"
            f"<b>Distance:</b> {seg['distance_km']} km<br>"
            f"<b>Cost:</b> {seg['composite_cost']}"
        )
        folium.Circle(
            location=midpoint,
            radius=100,
            color=color,
            fill=True,
            fill_opacity=0.4,
            popup=popup
        ).add_to(m)

    return m

