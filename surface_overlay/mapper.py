import json
import geopandas as gpd
import pydeck as pdk

# Load roads GeoJSON once (adjust path if needed)
def load_roads(path="data/roads.geojson"):
    return gpd.read_file(path)

# Define filters for road types
def filter_roads(roads_gdf, road_type):
    if road_type == "Dirt Roads":
        return roads_gdf[roads_gdf["surface"].str.lower() == "dirt"]
    elif road_type == "Paved Roads":
        return roads_gdf[roads_gdf["surface"].str.lower() == "paved"]
    else:
        return roads_gdf  # return all

# Render roads as Pydeck layer
def draw_roads_layer(filtered_roads_gdf, color=[200, 100, 50]):
    if filtered_roads_gdf.empty:
        return None

    # Convert to GeoJSON if needed
    geojson_data = filtered_roads_gdf.__geo_interface__

    layer = pdk.Layer(
        "GeoJsonLayer",
        data=geojson_data,
        get_line_color=color,
        get_line_width=4,
        pickable=True
    )
    return layer

