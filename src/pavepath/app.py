# utils/app.py

import streamlit as st
from route_optimizer import optimize_route
from utils.geocoder import geocode_location
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title="PavePath Hazard Routing", layout="wide")
st.title("🚧 PavePath Hazard-Aware Routing")

# Address inputs
start_location = st.text_input("Start location", value="Anaheim, CA")
end_location   = st.text_input("End location", value="Menifee, CA")

if st.button("Generate Route"):
    # Geocode first
    start_lat, start_lon = geocode_location(start_location)
    end_lat, end_lon     = geocode_location(end_location)

    if None in (start_lat, start_lon, end_lat, end_lon):
        st.error("Could not geocode one or both locations. Please check the addresses.")
        st.stop()

    # Now pass numeric coords to the optimizer
    locations = [(start_lat, start_lon), (end_lat, end_lon)]
    result = optimize_route(locations, mode="driving")

    # Map
    m = folium.Map(location=[start_lat, start_lon], zoom_start=11)
    for seg in result["segments"]:
        color = "red" if seg["hazard_score"] > 0.7 else "orange" if seg["hazard_score"] > 0.4 else "green"
        folium.PolyLine(
            locations=[seg["from"], seg["to"]],
            color=color,
            weight=5,
            tooltip=f"Hazard: {seg['hazard_score']}, Distance: {seg['distance_km']} km"
        ).add_to(m)
    folium_static(m)

    # Directions
    st.markdown("### 📋 Step-by-Step Directions")
    with st.expander("View Directions"):
        for i, step in enumerate(result["directions"]):
            st.markdown(f"**Step {i+1}:** {step['instruction']} — {step['distance_m']}m, {step['duration_s']}s")

