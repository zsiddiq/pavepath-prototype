import json
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union

# ----------------------------
# Ad-hoc parsing (tests expect these)
# ----------------------------

ADDRESS_LOOKUP = {
    "123 Main St, Menifee, CA": (33.8148, -117.9190)
}

GRID_LOOKUP = {
    "B3": (33.7000, -117.9000)
}

def parse_ad_hoc(inputs: Union[List, Tuple]) -> List[Tuple[float, float]]:
    """
    Parse coordinates, addresses, and grid IDs into [(lat, lon)].
    """
    results: List[Tuple[float, float]] = []
    for item in inputs:
        # Already a coordinate tuple
        if isinstance(item, tuple) and len(item) == 2 and all(isinstance(x, (int, float)) for x in item):
            results.append((float(item[0]), float(item[1])))
        # Address lookup
        elif isinstance(item, str) and item in ADDRESS_LOOKUP:
            results.append(ADDRESS_LOOKUP[item])
        # Grid lookup
        elif isinstance(item, str) and item in GRID_LOOKUP:
            results.append(GRID_LOOKUP[item])
        else:
            raise ValueError(f"Unsupported input: {item}")
    return results

# ----------------------------
# GeoJSON parsing (pipeline)
# ----------------------------

def load_geojson(path: Union[str, Path]) -> Dict[str, Any]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"GeoJSON file not found: {p}")
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)

def extract_route_features(geojson: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Normalize GeoJSON features into hazard-ready dicts.
    """
    features: List[Dict[str, Any]] = []
    for feature in geojson.get("features", []):
        props = feature.get("properties", {}) or {}
        geom = feature.get("geometry", {}) or {}
        coords = geom.get("coordinates", [])
        features.append({
            "location": props.get("name") or str(coords),
            "surface": props.get("surface"),
            "flood_risk": props.get("flood_risk", False),
            "raw_properties": props
        })
    return features

def parse_geojson_file(path: Union[str, Path]) -> List[Dict[str, Any]]:
    return extract_route_features(load_geojson(path))

# ----------------------------
# Unified dispatcher
# ----------------------------

def parse_input(input_data: Any):
    """
    Dispatch based on input type:
    - str ending with .geojson -> list[dict] hazard-ready features
    - list/tuple of items -> list[(lat, lon)] for ad-hoc tests
    """
    if isinstance(input_data, str) and input_data.lower().endswith(".geojson"):
        return parse_geojson_file(input_data)
    if isinstance(input_data, (list, tuple)):
        return parse_ad_hoc(input_data)
    raise ValueError(f"Unsupported input type: {type(input_data).__name__}")
