import streamlit as st
import pydeck as pdk
from surface_overlay import mapper
st.write("Full secrets:", st.secrets)
#MAPBOX_TOKEN = st.secrets["mapbox"]["token"]
MAPBOX_TOKEN = st.secrets["api_keys"]["mapbox"]

st.set_page_config(page_title="PavePath Routing Overlay", layout="wide")
st.title("PavePath: Routing App with Dirt/Paved Road Toggle")

# 🚦 UI Toggle
road_type = st.radio("Select road type to display:", ["Dirt Roads", "Paved Roads", "Both"])

# 📍 Load and filter roads
#roads_gdf = mapper.load_roads("data/roads.geojson")
import geopandas as gpd
from shapely.geometry import LineString

# Dummy data to verify pipeline
roads_gdf = gpd.GeoDataFrame({
    "road_type": ["dirt", "paved"],
    "geometry": [
        LineString([(-122.42, 37.78), (-122.43, 37.79)]),
        LineString([(-122.44, 37.78), (-122.45, 37.77)])
    ]
}, crs="EPSG:4326")

filtered_roads = mapper.filter_roads(roads_gdf, road_type)


#roads_gdf = load_roads_data()  # Load full GeoDataFrame
#filtered_roads = filter_roads(roads_gdf, road_type)  # Apply filter based on user input

# ✅ Quick Win 1: Optional debug table
if st.checkbox("Show road data table"):
    st.write(filtered_roads)

# ✅ Quick Win 2: Surface type breakdown (optional insights)
if st.checkbox("Show surface type breakdown"):
    st.write(roads_gdf["surface"].value_counts())

# ✅ Quick Win 3: Fallback message
if filtered_roads.empty:
    st.warning("No roads match the selected type. Try a different filter.")

# 🗺️ Draw map layer
road_layer = mapper.draw_roads_layer(filtered_roads)

# 🌍 Define map view (centered on sample coordinates—adjust as needed)
view_state = pdk.ViewState(
    latitude=33.8,  # Perris, CA area
    longitude=-117.2,
    zoom=11,
    pitch=0
)

# 🧭 Render map if layer exists
if road_layer:
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=view_state,
        layers=[road_layer]
    ))
else:
    st.warning("No roads to display for selected type.")

