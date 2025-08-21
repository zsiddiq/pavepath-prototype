import streamlit as st
from routing.google_maps import fetch_route
from routing.hazard_scoring import generate_hazard_scores
from routing.annotate import annotate_route_with_hazards
from utils.polyline_tools import decode_polyline
from utils.color_map import score_to_color
import folium
from streamlit_folium import folium_static

st.title("PavePath Hazard Overlay")

start = st.text_input("Start Location", "Redlands, CA")
end = st.text_input("End Location", "Ontario, CA")
api_key = st.secrets["GOOGLE_MAPS_API_KEY"]

if st.button("Generate Route"):
    steps = fetch_route(start, end, api_key)
    hazard_scores = generate_hazard_scores(steps)
    annotated = annotate_route_with_hazards(steps, hazard_scores)

    m = folium.Map(location=[steps[0]['start_location']['lat'], steps[0]['start_location']['lng']], zoom_start=12)
    for step in annotated:
        coords = decode_polyline(step['polyline']['points'])
        color = score_to_color(step['hazard_score'])
        folium.PolyLine(coords, color=color, weight=5).add_to(m)

    folium_static(m)
