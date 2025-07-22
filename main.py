import streamlit as st
import folium
from streamlit_folium import st_folium
from surface_overlay.mapper import load_road_data, style_dirt_road

# Load road data
road_data = load_road_data("data/roads.geojson")

# Create base map centered near Perris, CA
m = folium.Map(location=[33.799, -117.223], zoom_start=13)

# Add styled road segments
for feature in road_data["features"]:
    coords = feature["geometry"]["coordinates"]
    name = feature["properties"].get("name", "Unnamed")
    style = style_dirt_road(feature)

    folium.PolyLine(
        locations=[(lat, lon) for lon, lat in coords],
        tooltip=name,
        **style
    ).add_to(m)

# Display map in Streamlit
st.title("🛣️ Dirt Road Overlay Viewer")
st_folium(m, width=700, height=500)

