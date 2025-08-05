# input_parser.py

import re

def is_coordinate(item):
    """Check if item is a valid lat/lon pair."""
    try:
        lat, lon = map(float, item)
        return -90 <= lat <= 90 and -180 <= lon <= 180
    except:
        return False

def is_address(item):
    """Check if item looks like a physical address."""
    return isinstance(item, str) and "," in item and len(item.split()) > 2

def is_grid_id(item):
    """Check if item matches grid ID pattern (e.g., A1, B3)."""
    return isinstance(item, str) and re.match(r"^[A-Z]\d+$", item)

def parse_input(input_data):
    """
    Accepts a list of coordinates, addresses, or grid IDs.
    Returns a normalized list of (lat, lon) tuples.
    """
    parsed = []

    for item in input_data:
        if isinstance(item, tuple) and is_coordinate(item):
            parsed.append(item)

        elif is_address(item):
            # Stub geocoding logic
            print(f"Geocoding address: {item}")
            parsed.append((33.8148, -117.9190))  # Simulated result

        elif is_grid_id(item):
            # Stub grid resolution logic
            print(f"Resolving grid ID: {item}")
            parsed.append((33.7000, -117.9000))  # Simulated result

        else:
            raise ValueError(f"Unsupported input format: {item}")

    return parsed

# Example usage
if __name__ == "__main__":
    sample_input = [
        (33.8121, -117.9190),
        "123 Main St, Menifee, CA",
        "B3"
    ]
    print(parse_input(sample_input))
