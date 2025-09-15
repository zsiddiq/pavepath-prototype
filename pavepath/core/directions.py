# pavepath/core/directions.py

def extract_directions(route_json):
    directions = []
    for segment in route_json['features'][0]['properties']['segments']:
        for step in segment['steps']:
            directions.append({
                "instruction": step['instruction'],
                "distance_m": step['distance'],
                "duration_s": step['duration']
            })
    return directions
