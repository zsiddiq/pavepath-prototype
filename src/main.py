import os
import random
import pandas as pd
import streamlit as st
import pydeck as pdk
import streamlit.components.v1 as components

from surface_overlay import mapper
from pavepath.hazard_service import analyze_route
from pavepath.visualizer import visualize_route_scores

# 🔐 Secrets Handling
MAPBOX_TOKEN = None
try:
    MAPBOX_TOKEN = st.secrets["api_keys"]["mapbox"]
except Exception:
    MAPBOX_TOKEN = os.environ.get("MAPBOX_TOKEN")

if not MAPBOX_TOKEN:
    st.error("❌ Missing Mapbox token. Please set it in .streamlit/secrets.toml (local) "
             "or as an environment variable MAPBOX_TOKEN (Colab).")
    st.stop()

# 🖼️ Page Setup
st.set_page_config(page_title="PavePath Routing Overlay", layout="wide")
st.title("PavePath: Routing App with Dirt/Paved Road Toggle")

# 🚦 Road Type Selector (UI)
road_type_input = st.radio("Select road type to display:", ["Dirt Roads", "Paved Roads", "Both"])
road_type_mapped = {"Dirt Roads": "dirt", "Paved Roads": "paved", "Both": "both"}[road_type_input]

# 🗂️ Load Road Data
try:
    roads_gdf = mapper.load_roads("data/roads.geojson")
    if roads_gdf.empty:
        st.warning("Roads dataset is empty. Check data/roads.geojson.")
except FileNotFoundError:
    st.error("Roads file not found at data/roads.geojson. Add sample data or correct the path.")
    st.stop()
except Exception as e:
    st.error(f"Failed to load roads: {e}")
    st.stop()

# 🔍 Apply Filter
filtered_roads = mapper.filter_roads(roads_gdf, road_type_mapped)

# 🧰 Debugging + UI Feedback
if st.checkbox("Show road data table"):
    st.write(filtered_roads)

if st.checkbox("Show surface type breakdown"):
    st.write(roads_gdf["surface"].value_counts())

if filtered_roads.empty:
    st.warning("No roads match the selected type. Try a different filter.")

# 🎚️ User-defined risk threshold
risk_threshold = st.slider("Set risk threshold", min_value=0.0, max_value=10.0, value=6.0, step=0.5)

# 🧪 Generate Random Hazard Data
def generate_random_hazards():
    return {
        "weather": round(random.uniform(0, 10), 1),
        "road_condition": round(random.uniform(0, 10), 1),
        "traffic": round(random.uniform(0, 10), 1),
        "crime": round(random.uniform(0, 10), 1),
        "natural_disaster": round(random.uniform(0, 10), 1)
    }

route_data = [generate_random_hazards() for _ in range(len(filtered_roads))]
result = analyze_route(route_data, risk_threshold=risk_threshold)

# ⚠️ Inject hazard scores into filtered_roads for map coloring
scores = [s['score'] for s in result.get('segment_scores', [])]
if len(scores) == len(filtered_roads):
    filtered_roads = filtered_roads.copy()
    filtered_roads['hazard_score'] = scores
else:
    st.warning("Hazard score count doesn't match filtered road segments.")

# 📊 Show Hazard Scores
if st.checkbox("Show hazard scores"):
    st.write(result)

# 📈 Visualize Hazard Scores
if st.checkbox("Visualize hazard scores"):
    visualize_route_scores(result["segment_scores"])

# 🔍 Segment-Level Hazard Breakdown
if st.checkbox("Show segment-level hazard breakdown"):
    for segment in result["segment_scores"]:
        st.markdown(f"**Segment {segment['segment']}**")
        st.write(segment["hazards"])

# 📥 Download Hazard Report
if st.checkbox("Download hazard analysis as CSV"):
    df = pd.DataFrame(result["segment_scores"])
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Hazard Report",
        data=csv,
        file_name="hazard_analysis.csv",
        mime="text/csv"
    )

# 🗺️ Pydeck visualization
if not filtered_roads.empty:
    def linestring_to_coords(geom):
        if geom and geom.geom_type == "LineString":
            return [[lat, lon] for lon, lat in geom.coords]  # swap to [lat, lon]
        return []

    filtered_roads["path"] = filtered_roads.geometry.apply(linestring_to_coords)

    def score_to_color(score):
        if score is None:
            return [100, 100, 255]  # neutral blue
        if score < 3:
            return [0, 180, 80]     # green
        elif score < 6:
            return [255, 200, 0]    # yellow
        else:
            return [220, 60, 60]    # red

    filtered_roads["color"] = filtered_roads.get("hazard_score", pd.Series([None] * len(filtered_roads))).apply(score_to_color)

    layer = pdk.Layer(
        "PathLayer",
        filtered_roads,
        get_path="path",
        get_color="color",
        width_scale=1,
        width_min_pixels=3,
        pickable=True
    )

    view_state = pdk.ViewState(latitude=33.7, longitude=-117.2, zoom=10)
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, map_style=None))
else:
    st.info("No data to display on map.")

# 🌐 Google Maps Embed
if st.checkbox("Show Google Maps version"):
    try:
        with open("static/map_embed.html", "r") as f:
            html_code = f.read()
        components.html(html_code, height=600)
    except FileNotFoundError:
        st.error("Google Maps embed file not found at static/map_embed.html")
