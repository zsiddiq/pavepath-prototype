# pavepath-prototype

# 🛣️ PavePath Prototype

A modular routing and mapping tool designed for rural infrastructure planning, dirt road detection, and STR guest navigation. Built with Streamlit, Pydeck, and GeoJSON overlays, this prototype showcases early logic for surface-based alerting and map rendering.

---

## 🚀 Key Features

- **Surface Overlay Toggle**  
  Switch between paved and unpaved road views using a simple Streamlit UI toggle.

- **Alert Engine**  
  Prototype detection of dirt segments with optional logic for STR navigation warnings or trenching feasibility scores.

- **Modular Architecture**  
  Code is structured into independent components for alerts, overlays, and routing—ideal for rapid prototyping and incremental builds.

---

## 🗺️ Tech Stack

| Component   | Description                                  |
|------------|----------------------------------------------|
| Streamlit  | Lightweight web UI for toggling and display |
| Pydeck     | Map rendering using Deck.gl layers           |
| GeoJSON    | Sample surface metadata for road segments   |
| Markdown   | Persistent project notes (see `/docs/`)      |

---

## 🧪 Getting Started

### Requirements

```bash
pip install -r requirements.txt

**To Run the APP:**

streamlit run main.py

Project Structure:

├── main.py                      # Streamlit entry point
├── surface_overlay/mapper.py   # Overlay styling and filtering
├── alert_logic/engine.py       # Dirt detection logic
├── routing_engine/             # (Placeholder) Routing code
├── data/roads.geojson          # Sample surface metadata
├── docs/SDLC.md                # Tracker and next steps
├── .devcontainer/              # Optional dev setup
└── requirements.txt


sequenceDiagram
    participant User
    participant Frontend UI (Streamlit/Folium)
    participant Routing Service (Python microservice)
    participant Mapping API (e.g., OpenStreetMap, Mapbox)
    participant Data Store (optional)

    User->>Frontend UI: Enter location and routing query
    Frontend UI->>Routing Service: Submit request for route and map data
    Routing Service->>Mapping API: Fetch base map and route geometry
    Routing Service->>Data Store: (Optional) Log request or enrich with metadata
    Mapping API-->>Routing Service: Return raw map/route data
    Routing Service-->>Frontend UI: Send enriched map object
    Frontend UI-->>User: Display interactive map or download link


