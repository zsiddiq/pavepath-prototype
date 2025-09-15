import math
import openrouteservice
import streamlit as st
from pavepath.hazard_service import simulate_hazards_for_segment, score_segment
from pavepath.core.directions import extract_directions

# Tunable weights for composite cost function
HAZARD_WEIGHT = 0.7
DISTANCE_WEIGHT = 0.3

ORS_API_KEY = st.secrets["api_keys"]["ors"]

def haversine(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 6371  # Earth radius in km

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2)**2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def compute_segment_cost(start, end, mode="safe"):
    hazards = simulate_hazards_for_segment(start, end)
    hazard_score = score_segment(hazards)
    distance_km = haversine(start, end)

    if mode == "safe":
        cost = hazard_score * HAZARD_WEIGHT + distance_km * DISTANCE_WEIGHT
    else:
        cost = distance_km

    return round(cost, 2), hazard_score, distance_km

def get_driving_segments(origin, destination):
    client = openrouteservice.Client(key=ORS_API_KEY)

    origin_coords = (origin[1], origin[0])
    destination_coords = (destination[1], destination[0])

    response = client.directions(
        coordinates=[origin_coords, destination_coords],
        profile='driving-car',
        format='geojson'
    )

    geometry = response['features'][0]['geometry']['coordinates']
    segments = [
        {"from": (coord[1], coord[0]), "to": (geometry[i+1][1], geometry[i+1][0])}
        for i, coord in enumerate(geometry[:-1])
    ]

    directions = extract_directions(response)
    print("Extracted directions:")
    for d in directions:
        print(d["instruction"])

    return segments, directions

