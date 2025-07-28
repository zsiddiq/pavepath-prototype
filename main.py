import streamlit as st
import pydeck as pdk
import geopandas as gpd
from shapely.geometry import LineString
from surface_overlay import mapper

# 🔐 Secrets
st.write("Full secrets:", st.secrets)
MAPBOX_TOKEN = st.secrets["api_keys"]["mapbox"]

# 🖼️ Page Setup
st.set_page_config(page_title="PavePath Routing Overlay", layout="wide")
st.title("PavePath: Routing App with Dirt/Paved Road Toggle")

# 🚦 Road Type Selector (UI)
road_type_input = st.radio("Select road type to display:", ["Dirt Roads", "Paved Roads", "Both"])

# 🧠 Internal Mapping
road_type_mapped = {
    "Dirt Roads": "dirt",
    "Paved Roads": "paved",
    "Both": "both"
}[road_type_input]

# 🧪 Dummy Data
roads_gdf = gpd.GeoDataFrame({
    "road_type": ["dirt", "paved"],
    "surface": ["dirt", "paved"],  # ✅ lowercase values
    "geometry": [
        LineString([(-122.42, 37.78), (-122.43, 37.79)]),
        LineString([(-122.44, 37.78), (-122.45, 37.77)])
    ]
}, crs="EPSG:4326")

# 🔍 Apply Filter
filtered_roads = mapper.filter_roads(roads_gdf, road_type_mapped)

# 🧰 Debugging + UI Feedback
if st.checkbox("Show road data table"):
    st.write(filtered_roads)

if st.checkbox("Show surface type breakdown"):
    st.write(roads_gdf["surface"].value_counts())

if filtered_roads.empty:
    st.warning("No roads match the selected type. Try a different filter.")

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
