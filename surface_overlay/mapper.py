import json

def load_road_data(filepath):
    """Loads GeoJSON-style road data"""
    with open(filepath, 'r') as f:
        return json.load(f)

def style_dirt_road(feature):
    """Return style dict for dirt roads"""
    return {
        'color': 'brown',
        'weight': 3,
        'opacity': 0.8
    } if feature['properties'].get('surface') == 'unpaved' else {
        'color': 'gray',
        'weight': 2,
        'opacity': 0.3
    }
