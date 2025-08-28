import streamlit as st
from streamlit_folium import st_folium
from pavepath.route_optimizer import optimize_route
from pavepath.visualizer import render_route_map

st.title("PavePath: Hazard-Aware Route Viewer")

# Initialize session state
if "route_data" not in st.session_state:
    st.session_state.route_data = None

# Input fields for origin and destination
with st.form("route_form"):
    origin = st.text_input("Enter origin coordinates (lat, lon)", "33.8121, -117.9190")
    destination = st.text_input("Enter destination coordinates (lat, lon)", "34.0522, -118.2437")
    submitted = st.form_submit_button("Generate Route")

# Parse and generate route
if submitted:
    try:
        origin_coords = tuple(map(float, origin.split(",")))
        destination_coords = tuple(map(float, destination.split(",")))
        locations = [origin_coords, destination_coords]
        st.session_state.route_data = optimize_route(locations, mode="driving")
    except:
        st.error("Invalid coordinates. Please enter as lat, lon")

# Display route map and hazard summary
if st.session_state.route_data:
    st.subheader("Optimized Route with Hazard Overlays")
    st_folium(render_route_map(st.session_state.route_data), width=700, height=500)

    # Optional hazard score summary
    segments = st.session_state.route_data.get("segments", [])
    total_score = sum(seg.get("hazard_score", 0) for seg in segments)
    st.markdown(f"**Total Hazard Score:** {round(total_score, 2)}")

    # Flag high-risk segments
    high_risk = [seg for seg in segments if seg.get("hazard_score", 0) > 0.7]
    if high_risk:
        st.warning(f"{len(high_risk)} segment(s) flagged as high-risk.")

     # 🔍 Segment-Level Debug View
    with st.expander("Segment-Level Hazard Scores"):
        for i, seg in enumerate(segments):
            score = round(seg.get("hazard_score", 0), 2)
            st.write(f"Segment {i+1}: {seg.get('start')} → {seg.get('end')} | Score: {score}")
