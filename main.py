import streamlit as st
import pydeck as pdk
from surface_overlay import mapper  # assuming mapper.py is in surface_overlay/

st.set_page_config(page_title="PavePath Routing Overlay", layout="wide")
st.title("PavePath: Routing App with Dirt/Paved Road Toggle")

# 🚦 UI Toggle
road_type = st.radio("Select road type to display:", ["Dirt Roads", "Paved Roads", "Both"])

# 📍 Load and filter roads
roads_gdf = mapper.load_roads("data/roads.geojson")
filtered_roads = mapper.filter_roads(roads_gdf, road_type)

st.write(filtered_roads)  # 👈 See what you've got post-filter

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

