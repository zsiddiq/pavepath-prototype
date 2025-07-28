import json
import geopandas as gpd
import pydeck as pdk
import folium

# --- Data Loading ---
def load_roads(path="data/roads.geojson"):
    roads_gdf = gpd.read_file(path)
    print(roads_gdf.columns)  # Should include 'surface'
    print(roads_gdf.head())   # Quick preview
    return roads_gdf

# --- Road Type Filtering ---
def filter_roads(roads_gdf, surface_type="both"):
    if surface_type == "dirt":
        return roads_gdf[roads_gdf["surface"] == "dirt"]
    elif surface_type == "paved":
        return roads_gdf[roads_gdf["surface"] == "paved"]
    else:  # "both"
        return roads_gdf

# --- Folium Map Rendering ---
def add_roads_to_map(map_obj, roads_gdf):
    surface_colors = {
        "dirt": "brown",
        "paved": "gray"
    }
    for _, row in roads_gdf.iterrows():
        coords = [(pt[1], pt[0]) for pt in row.geometry.coords]  # Convert (lon, lat) to (lat, lon)
        color = surface_colors.get(row["surface"], "blue")
        folium.PolyLine(coords, color=color, weight=3).add_to(map_obj)

def render_folium_map(surface_type="both"):
    roads = load_roads()
    filtered = filter_roads(roads, surface_type)
    fmap = folium.Map(location=[33.833, -117.19], zoom_start=15)
    add_roads_to_map(fmap, filtered)
    fmap.save("map.html")

# --- Pydeck Layer Rendering ---
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
if __name__ == "__main__":
    render_folium_map("both")  # or use a parameter like "simple", "route", etc.
