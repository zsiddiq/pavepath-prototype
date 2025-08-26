import streamlit as st
from streamlit_folium import st_folium
from pavepath.route_optimizer import optimize_route
from pavepath.visualizer import render_route_map

sample_locations = [
    (33.8121, -117.9190),  # Anaheim
    (34.0522, -118.2437),  # Los Angeles
    (33.7701, -118.1937),  # Long Beach
    (33.8358, -117.9143),  # Santa Ana
]

st.title("PavePath: Hazard-Aware Route Viewer")

# Initialize session state
if "route_data" not in st.session_state:
    st.session_state.route_data = None

# Button to generate route
if st.button("Generate Route"):
    st.session_state.route_data = optimize_route(sample_locations, mode="safe")

# Display map if route exists
if st.session_state.route_data:
    st_folium(render_route_map(st.session_state.route_data), width=700, height=500)

