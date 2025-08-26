import streamlit as st
from streamlit_folium import st_folium
from pavepath.route_optimizer import optimize_route
from visualizer import render_route_map

# Sample input — replace with dynamic input later
sample_locations = [
    (33.8121, -117.9190),  # Anaheim
    (34.0522, -118.2437),  # Los Angeles
    (33.7701, -118.1937),  # Long Beach
    (33.8358, -117.9143),  # Santa Ana
]

# Run optimizer
route_data = optimize_route(sample_locations, mode="safe")

# Display map
st.title("PavePath: Hazard-Aware Route Viewer")
st_folium(render_route_map(route_data), width=700, height=500)
