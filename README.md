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

where does mapbox fit into this?
Mapbox fits squarely between your Routing Service and Frontend UI, acting as both a mapping API and potentially a rendering engine — depending on how deeply you integrate it.

sequenceDiagram
    participant User
    participant Frontend UI (Streamlit / Folium / Pydeck)
    participant Routing Service (Python microservice)
    participant Mapbox API
    participant Data Store (optional)

    User->>Frontend UI: Enter location and routing query
    Frontend UI->>Routing Service: Submit coordinates, profile, and display parameters
    Routing Service->>Mapbox API: Request route geometry and style layers
    Routing Service->>Data Store: Log request or update metrics
    Mapbox API-->>Routing Service: Return route and tile data
    Routing Service-->>Frontend UI: Pass data as map layer or URL
    Frontend UI-->>User: Render map with interactive Mapbox layers

Mapbox’s roles could include:

Routing: If you use their Directions API for driving, walking, or cycling paths.

Base mapping: Their tile layers and styling let you visualize terrain, streets, etc.

Rendering: You can embed maps directly via Mapbox GL JS or Streamlit plugins.

Customization: Offers dynamic styling, zoom levels, and overlays from backend logic.

If you’re prototyping with Folium, it’s more static, while Pydeck or Mapbox GL opens full interactivity.

classDiagram
    class RouteRequest {
        +origin: str
        +destination: str
        +profile: str
        +validate()
    }

    class RoutingService {
        +route_algorithm: str
        +get_route(request: RouteRequest): MapObject
    }

    class MapObject {
        +geometry: GeoJSON
        +style: dict
        +render()
    }

    class MapboxAdapter {
        +api_key: str
        +fetch_tiles(): TileData
        +fetch_route(): GeoJSON
    }

    RoutingService --> RouteRequest
    RoutingService --> MapObject
    RoutingService --> MapboxAdapter
This shows how a user-submitted RouteRequest flows through a service that talks to Mapbox and produces a MapObject for rendering.

flowchart TD
    A[Start: User opens app] --> B[Enter route parameters]
    B --> C{Is input valid?}
    C -- Yes --> D[Submit to Routing Service]
    C -- No --> E[Show error message]
    E --> B

    D --> F[Call Mapbox API for route and tiles]
    F --> G[Receive route geometry and map tiles]
    G --> H[Render map in UI]
    H --> I{Download or view?}
    I -- View --> J[Display interactive map]
    I -- Download --> K[Generate map file]
    J --> L[End]
    K --> L

This style helps track:

User decisions (e.g., view vs download)

Validation points

Backend interactions and API dependencies

End-user outcomes

**************************************************

Unified Modeling Language (UML) offers a full suite of diagram types, each tailored to a specific aspect of system design — from static structure to dynamic behavior. Here's a complete rundown grouped by purpose, with brief context for how each might apply to your modular builds like PavePath:

🏗 Structural Diagrams (Static architecture)
These describe what your system is, not how it behaves.

Diagram Type	Purpose	Example in Your Context
Class Diagram	Shows system classes, attributes, and relationships	RoutingService, MapboxAdapter, GuestProfileManager
Object Diagram	Snapshot of instances and their links at a given moment	State view of active guest tools or route components
Component Diagram	High-level view of modules and interfaces	Microservice packages, STR widget injection points
Package Diagram	Organization of classes and components into packages	Mapping module vs routing logic vs STR customization layer
Deployment Diagram	Shows nodes (servers, containers) and artifacts	Where each service/API lives in your infrastructure
Composite Structure Diagram	Internal parts of a class and their collaborations	Route rendering class showing nested behaviors

🔄 Behavioral Diagrams (Interactions and flows)

Diagram Type	Purpose	Example in Your Context
Use Case Diagram	Captures user goals and system responses	STR guest creates custom itinerary → host approves → map sent
Sequence Diagram	Timeline-based interaction between system components	As we’ve built already for routing and Mapbox flow
Activity Diagram	Workflow with decisions and loops	Route submission → validation → render/download
State Machine Diagram	State transitions triggered by events	Orchard zone shifts from "inactive" to "harvest-ready"
Communication Diagram	Message passing and interactions between objects	Similar to sequence, but more network-style visualization
Interaction Overview	Overview linking multiple sequences	High-level guest tool interaction combining multiple flows
Timing Diagram	Time-bound interactions and behaviors	Sensor reading intervals, refresh cycles for route maps

🎯 Additional diagrams (Less common but useful in niche scenarios)

Diagram Type	Purpose	Contextual Use
Profile Diagram	Custom extensions to UML (advanced metamodeling)	Rarely needed unless extending UML in domain-specific ways
Information Flow Diagram	How information moves between elements	Useful for guest metadata flowing through STR personalization
If you'd like, I can walk through which of these would be most valuable for your short-term goals vs architectural clarity. We can even build a diagnostic flow: "What are you designing → What diagrams help visualize it best." Want to map that out?
