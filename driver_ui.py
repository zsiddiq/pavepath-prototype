import streamlit as st
from streamlit_folium import st_folium
from pavepath.route_optimizer import optimize_route
from pavepath.visualizer import render_route_map

sample_locations = [
    (33.8121, -117.9190),
    (34.0522, -118.2437),
    (33.7701, -118.1937),
    (33.8358, -117.9143),
]

st.title("PavePath: Hazard-Aware Route Viewer")

if st.button("Generate Route"):
    route_data = optimize_route(sample_locations, mode="safe")
    st_folium(render_route_map(route_data), width=700, height=500)
