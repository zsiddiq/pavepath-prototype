import json
import geopandas as gpd
import pydeck as pdk

# Load roads GeoJSON once (adjust path if needed)
def load_roads(path="data/roads.geojson"):
    roads_gdf = gpd.read_file(path)        # Load the file first
    print(roads_gdf.columns)               # Check available columns
    print(roads_gdf.head())                # See sample rows
    return roads_gdf                      # Return for use in rest of script


# Define filters for road types
def filter_roads(gdf, road_type):
    surface_column = gdf["surface"].str.lower()
    if road_type == "dirt":
        return gdf[surface_column == "dirt"]
    elif road_type == "paved":
        return gdf[surface_column == "paved"]
    else:
        return gdf




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


