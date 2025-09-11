import streamlit as st
from streamlit_folium import st_folium
from pavepath.route_optimizer import optimize_route
from pavepath.visualizer import render_route_map
from pavepath.utils.geocoder import geocode_location
from pavepath.utils.display import mask_key  # NEW: extracted helper

# Load API key from Streamlit Secrets
API_KEY = st.secrets.get("OPENCAGE_API_KEY", None)

# 🔔 Warn if secrets not injected
if not API_KEY:
    st.warning("⚠️ OPENCAGE_API_KEY not loaded from Streamlit Secrets. Using manual input fallback.")

# Page setup (place early)
st.set_page_config(
    page_title="PavePath: Hazard-Aware Routing",
    layout="centered",  # Better for mobile readability
)

st.title("🚧 PavePath: Hazard-Aware Route Viewer")

# 🔧 Diagnostics panel with manual override
with st.expander("🔧 Env diagnostics"):
    st.write("**OPENCAGE_API_KEY from secrets:**", mask_key(API_KEY))

    manual_key = st.text_input("🔑 Manually enter API key (for testing)", "")
    test_location = st.text_input("Test a location", "Anaheim, CA")

    if st.button("🧪 Run Geocoder Test"):
        key_to_use = manual_key if manual_key else API_KEY
        latlon = geocode_location(test_location, api_key=key_to_use, debug=True)
        st.write("Test result:", latlon)

# Initialize session state
if "route_data" not in st.session_state:
    st.session_state.route_data = None

# Location-based input form
with st.form("route_form"):
    origin = st.text_input("Enter origin location", "Anaheim, CA")
    destination = st.text_input("Enter destination location", "Menifee, CA")
    submitted = st.form_submit_button("📍 Generate Route")

# Route generation
if submitted:
    key_to_use = manual_key if manual_key else API_KEY
    try:
        origin_coords = geocode_location(origin, api_key=key_to_use, debug=True)
        destination_coords = geocode_location(destination, api_key=key_to_use, debug=True)

        if None in origin_coords or None in destination_coords:
            st.error("Could not geocode one or both locations.")
            st.stop()

        locations = [origin_coords, destination_coords]
        st.session_state.route_data = optimize_route(locations, mode="driving")

    except Exception as e:
        st.error(f"Error generating route: {e}")

# Route display
if st.session_state.route_data:
    st.subheader("🗺️ Optimized Route with Hazard Overlays")
    st_folium(render_route_map(st.session_state.route_data), width=350, height=400)

    segments = st.session_state.route_data.get("segments", [])
    total_score = sum(seg.get("hazard_score", 0) for seg in segments)
    st.markdown(f"**Total Hazard Score:** {round(total_score, 2)}")

    high_risk = [seg for seg in segments if seg.get("hazard_score", 0) > 0.7]
    if high_risk:
        st.warning(f"{len(high_risk)} segment(s) flagged as high-risk.")

    with st.expander("📊 Segment-Level Hazard Scores"):
        for i, seg in enumerate(segments):
            score = round(seg.get("hazard_score", 0), 2)
            st.write(f"Segment {i+1}: {seg.get('from')} → {seg.get('to')} | Score: {score}")

    directions = st.session_state.route_data.get("directions", [])
    if directions:
        st.subheader("📍 Step-by-Step Directions")
        with st.expander("View Directions"):
            for i, step in enumerate(directions):
                st.markdown(f"**Step {i+1}:** {step['instruction']} — {step['distance_m']}m, {step['duration_s']}s")
    else:
        st.info("No directions available for this route.")

