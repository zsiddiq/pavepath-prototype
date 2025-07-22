import streamlit as st
from alert_logic.engine import generate_alert

st.title("🛣️ PavePath Dirt Road Aware Routing")

destination = st.text_input("Enter your destination address")

# For demo purposes, use mock route segments
mock_route = ["Maple St", "Dusty Road", "Main Blvd"]
known_dirt_roads = ["Dusty Road"]

if destination:
    alert = generate_alert(mock_route, known_dirt_roads)
    if alert["message"]:
        st.warning(alert["message"])
        st.button("Reroute")
