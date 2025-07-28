import json
import geopandas as gpd
import pydeck as pdk

# Load roads GeoJSON once (adjust path if needed)
def load_roads(path="data/roads.geojson"):
    return gpd.read_file(path)

# Define filters for road types
def filter_roads(roads_gdf, road_type):
    surface_column = roads_gdf["surface"].str.lower()

    if road_type == "Dirt Roads":
        return roads_gdf[surface_column == "unpaved"]
    elif road_type == "Paved Roads":
        return roads_gdf[surface_column == "paved"]
    else:
        return roads_gdf



# Render roads as Pydeck layer
def draw_roads_layer(filtered_roads_gdf, color=[200, 100, 50]):
    geojson_data = filtered_roads_gdf.__geo_interface__

    layer = pdk.Layer(
        "GeoJsonLayer",
        data=geojson_data,
        get_line_color=color,
        get_line_width=4,
        pickable=True,
        auto_highlight=True,
        get_tooltip={'text': 'Road: {name}\\nSurface: {surface}'}
    )
    return layer


