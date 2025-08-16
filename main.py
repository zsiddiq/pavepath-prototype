import streamlit as st
import pydeck as pdk
import geopandas as gpd
from shapely.geometry import LineString
from surface_overlay import mapper

# 🧠 Hazard Analysis Imports
from pavepath.hazard_service import analyze_route
from pavepath.visualizer import visualize_route_scores
import random
import pandas as pd

# 🔐 Secrets
st.write("Full secrets:", st.secrets)
MAPBOX_TOKEN = st.secrets["api_keys"]["mapbox"]

# 🖼️ Page Setup
st.set_page_config(page_title="PavePath Routing Overlay", layout="wide")
st.title("PavePath: Routing App with Dirt/Paved Road Toggle")

# 🚦 Road Type Selector (UI)
road_type_input = st.radio("Select road type to display:", ["Dirt Roads", "Paved Roads", "Both"])

road_type_mapped = {
    "Dirt Roads": "dirt",
    "Paved Roads": "paved",
    "Both": "both"
}[road_type_input]

# 🗂️ Load Road Data
roads_gdf = mapper.load_roads("data/roads.geojson")

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

# ⚠️ Analyze Hazards with Custom Threshold
result = analyze_route(route_data, risk_threshold=risk_threshold)

# 🎨 Inject hazard scores into filtered_roads for map coloring
scores = [s['score'] for s in result['segment_scores']]
filtered_roads = filtered_roads.copy()
filtered_roads['hazard_score'] = scores


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

# 🗺️ Map Rendering
road_layer = mapper.draw_roads_layer(filtered_roads)

view_state = pdk.ViewState(
    latitude=33.8,  # Perris, CA
    longitude=-117.2,
    zoom=11,
    pitch=0
)

if road_layer:
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=view_state,
        layers=[road_layer]
    ))
else:
    st.warning("No roads to display for selected type.")
