import json
from typing import List, Dict, Any, Union
from pathlib import Path


def load_geojson(path: Union[str, Path]) -> Dict[str, Any]:
    """
    Load a GeoJSON file into a Python dictionary.

    Args:
        path: Path to the GeoJSON file.

    Returns:
        Parsed GeoJSON as a Python dict.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"GeoJSON file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_route_features(geojson: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extract route features from a GeoJSON dict and normalize them
    into hazard-ready dictionaries.

    Args:
        geojson: Parsed GeoJSON dict.

    Returns:
        List of dicts with normalized route features.
    """
    features = []
    for feature in geojson.get("features", []):
        props = feature.get("properties", {})
        coords = feature.get("geometry", {}).get("coordinates", [])

        # Normalize into hazard-ready schema
        features.append({
            "location": props.get("name") or str(coords),
            "surface": props.get("surface"),
            "flood_risk": props.get("flood_risk", False),
            "raw_properties": props  # keep full props for debugging/extensibility
        })
    return features


def parse_input(path: Union[str, Path]) -> List[Dict[str, Any]]:
    """
    Convenience wrapper: load a GeoJSON file and extract normalized route features.

    Args:
        path: Path to the GeoJSON file.

    Returns:
        List of hazard-ready route dicts.
    """
    geojson = load_geojson(path)
    return extract_route_features(geojson)


# Optional: provider-specific stubs for future extension
def parse_google_maps_response(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Parse a Google Maps Directions API response into hazard-ready dicts.
    Placeholder for future implementation.
    """
    # TODO: implement once Google Maps integration is active
    return []


def parse_osm_response(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Parse an OSM API response into hazard-ready dicts.
    Placeholder for future implementation.
    """
    # TODO: implement once OSM integration is active
    return []
