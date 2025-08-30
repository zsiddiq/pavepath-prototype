import streamlit as st
from route_optimizer import optimize_route
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title="PavePath Hazard Routing", layout="wide")
st.title("🚧 PavePath Hazard-Aware Routing")

# Input fields
start_lat = st.number_input("Start Latitude", value=33.680984)
start_lon = st.number_input("Start Longitude", value=-117.170700)
end_lat = st.number_input("End Latitude", value=33.835293)
end_lon = st.number_input("End Longitude", value=-117.914505)

locations = [(start_lat, start_lon), (end_lat, end_lon)]

if st.button("Generate Route"):
    result = optimize_route(locations, mode="driving")

    # Map initialization
    m = folium.Map(location=[start_lat, start_lon], zoom_start=11)

    # Draw segments with hazard color
    for seg in result["segments"]:
        folium.PolyLine(
            locations=[seg["from"], seg["to"]],
            color="red" if seg["hazard_score"] > 0.7 else "orange" if seg["hazard_score"] > 0.4 else "green",
            weight=5,
            tooltip=f"Hazard: {seg['hazard_score']}, Distance: {seg['distance_km']} km"
        ).add_to(m)

    folium_static(m)

    # Step-by-step directions
    st.markdown("### 📋 Step-by-Step Directions")
    with st.expander("View Directions"):
        for i, step in enumerate(result["directions"]):
            st.markdown(f"**Step {i+1}:** {step['instruction']} — {step['distance_m']}m, {step['duration_s']}s")
