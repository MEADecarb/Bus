import folium
import requests
import json

# Define a color palette
color_palette = ["#2C557E", "#fdda25", "#B7DCDF", "#000000"]  # Fixed color format

# Create a base map centered over Maryland
m = folium.Map(location=[39.0458, -76.6413], zoom_start=8)

def add_geojson_from_url(geojson_url, name, color, map_obj):
    feature_group = folium.FeatureGroup(name=name)
    style_function = lambda x: {'fillColor': color, 'color': color}
    response = requests.get(geojson_url)
    if response.status_code == 200:
        geojson_data = response.json()

        # Debug: print the first 1000 characters of the data to understand its structure
        print(json.dumps(geojson_data, indent=2)[:1000])

        # Ensure that the data is in the expected GeoJSON format
        if 'features' in geojson_data:
            try:
                # Retrieve all field names from the properties of the first feature
                all_fields = list(geojson_data['features'][0]['properties'].keys())

                geojson_layer = folium.GeoJson(
                    geojson_data,
                    style_function=style_function
                ).add_to(feature_group)

                # Add a popup that shows all fields
                popup = folium.GeoJsonPopup(fields=all_fields, labels=True)
                geojson_layer.add_child(popup)

                feature_group.add_to(map_obj)
            except Exception as e:
                print(f"Error adding GeoJSON layer for {name}: {e}")
        else:
            print(f"Data for {name} does not seem to be in the expected GeoJSON format.")
    else:
        print(f"Failed to retrieve {name}. Status code: {response.status_code}")

# Add each GeoJSON source as a separate feature group with a color, label, and pop-up
github_geojson_sources = [
    ("https://services1.arcgis.com/Hp6G80Pky0om7QvQ/arcgis/rest/services/Retail_Service_Territories/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson", "Electric Retail Service Territories"),
    ("https://services.arcgis.com/njFNhDsUCentVYJW/arcgis/rest/services/MDOT_SHA_County_Boundaries/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson", "MDOT SHA County Boundaries"),
    ("https://meadecarb.github.io/GEO/map.geojson", "MD HB550 Overburdened Census Tracts")
]

for i, (url, name) in enumerate(github_geojson_sources):
    color = color_palette[i % len(color_palette)]
    add_geojson_from_url(url, name, color, m)

# Add Layer Control to toggle feature groups
folium.LayerControl().add_to(m)

# Display the map
m
