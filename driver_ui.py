import streamlit as st
from streamlit_folium import st_folium
from pavepath.route_optimizer import optimize_route
from pavepath.visualizer import render_route_map
from pavepath.utils.geocoder import geocode_location

# Load API key from Streamlit Secrets
API_KEY = st.secrets.get("OPENCAGE_API_KEY", None)

# 🔧 Diagnostics panel
with st.expander("🔧 Env diagnostics"):
    def _mask(v):
        return (v[:4] + "..." + v[-4:]) if v and len(v) > 8 else ("set" if v else "None")
    st.write("**OPENCAGE_API_KEY:**", _mask(API_KEY))

    test_location = st.text_input("Test a location", "Anaheim, CA")
    if st.button("Test Geocode"):
        lat, lon = geocode_location(test_location, api_key=API_KEY, debug=True)
        st.write(f"Result: {lat}, {lon}")

# Page setup
st.set_page_config(page_title="PavePath: Hazard-Aware Routing", layout="wide")
st.title("🚧 PavePath: Hazard-Aware Route Viewer")

# Initialize session state
if "route_data" not in st.session_state:
    st.session_state.route_data = None

# Location-based input form
with st.form("route_form"):
    origin = st.text_input("Enter origin location", "Anaheim, CA")
    destination = st.text_input("Enter destination location", "Menifee, CA")
    submitted = st.form_submit_button("Generate Route")

# Route generation
if submitted:
    try:
        origin_coords = geocode_location(origin, api_key=API_KEY, debug=True)
        destination_coords = geocode_location(destination, api_key=API_KEY, debug=True)

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
    st_folium(render_route_map(st.session_state.route_data), width=700, height=500)

    segments = st.session_state.route_data.get("segments", [])
    total_score = sum(seg.get("hazard_score", 0) for seg in segments)
    st.markdown(f"**Total Hazard Score:** {round(total_score, 2)}")

    high_risk = [seg for seg in segments if seg.get("hazard_score", 0) > 0.7]
