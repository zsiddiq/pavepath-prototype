import streamlit as st
from streamlit_folium import st_folium
from pavepath.route_optimizer import optimize_route
from pavepath.visualizer import render_route_map
from pavepath.utils.geocoder import geocode_location

from pavepath.utils.geocoder import geocode_location
import os
from dotenv import load_dotenv

# Ensure env is loaded in Streamlit
load_dotenv()

import os
import streamlit as st

# Load from GitHub Actions or Streamlit Cloud env
API_KEY = os.getenv("OPENCAGE_API_KEY")

with st.expander("🔧 Env diagnostics"):
    def _mask(v):
        return (v[:4] + "..." + v[-4:]) if v and len(v) > 8 else ("set" if v else "None")
    st.write("**OPENCAGE_API_KEY:**", _mask(API_KEY))


st.subheader("🔍 Geocoder Test")
test_location = st.text_input("Test a location", "Anaheim, CA")
if st.button("Test Geocode"):
    lat, lon = geocode_location(test_location)
    st.write(f"Result: {lat}, {lon}")


st.set_page_config(page_title="PavePath: Hazard-Aware Routing", layout="wide")
st.title("🚧 PavePath: Hazard-Aware Route Viewer")

# Initialize session state
if "route_data" not in st.session_state:
    st.session_state.route_data = None

# Input fields for origin and destination
with st.form("route_form"):
    #origin = st.text_input("Enter origin coordinates (lat, lon)", "33.8121, -117.9190")
    #destination = st.text_input("Enter destination coordinates (lat, lon)", "34.0522, -118.2437")
    origin = st.text_input("Enter origin location", "Anaheim, CA")
    destination = st.text_input("Enter destination location", "Menifee, CA")
    submitted = st.form_submit_button("Generate Route")

# Parse and generate route
if submitted:
    from pavepath.utils.geocoder import geocode_location   # Adjust import if needed

    try:
        origin_coords = geocode_location(origin)
        destination_coords = geocode_location(destination)
        if None in origin_coords or None in destination_coords:
            st.error("Could not geocode one or both locations.")
            st.stop()
        locations = [origin_coords, destination_coords]
        st.session_state.route_data = optimize_route(locations, mode="driving")
    except Exception as e:
        st.error(f"Error generating route: {e}")

   # try:
    #    origin_coords = tuple(map(float, origin.split(",")))
    #    destination_coords = tuple(map(float, destination.split(",")))
    #    locations = [origin_coords, destination_coords]
    #    st.session_state.route_data = optimize_route(locations, mode="driving")
    #except:
      #  st.error("Invalid coordinates. Please enter as lat, lon")

# Display route map and hazard summary
if st.session_state.route_data:
    st.subheader("🗺️ Optimized Route with Hazard Overlays")
    st_folium(render_route_map(st.session_state.route_data), width=700, height=500)

    segments = st.session_state.route_data.get("segments", [])
    total_score = sum(seg.get("hazard_score", 0) for seg in segments)
    st.markdown(f"**Total Hazard Score:** {round(total_score, 2)}")

    high_risk = [seg for seg in segments if seg.get("hazard_score", 0) > 0.7]
    if high_risk:
        st.warning(f"{len(high_risk)} segment(s) flagged as high-risk.")

    # 🔍 Segment-Level Debug View
    with st.expander("📊 Segment-Level Hazard Scores"):
        for i, seg in enumerate(segments):
            score = round(seg.get("hazard_score", 0), 2)
            st.write(f"Segment {i+1}: {seg.get('from')} → {seg.get('to')} | Score: {score}")

    # 📋 Step-by-Step Directions
    directions = st.session_state.route_data.get("directions", [])
    if directions:
        st.subheader("📍 Step-by-Step Directions")
        with st.expander("View Directions"):
            for i, step in enumerate(directions):
                st.markdown(f"**Step {i+1}:** {step['instruction']} — {step['distance_m']}m, {step['duration_s']}s")
    else:
        st.info("No directions available for this route.")
