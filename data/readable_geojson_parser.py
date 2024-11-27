import json
import pandas as pd

# Load the GeoJSON data
with open('local-area-boundary.geojson', 'r') as f:
    geojson_data = json.load(f)

# Extract features
features = geojson_data['features']

# Create lists to store the parsed data
names = []
coordinates = []
geo_points = []

# Parse the features
for feature in features:
    name = feature['properties']['name']
    coordinate = feature['geometry']['coordinates']
    geo_point = feature['properties']['geo_point_2d']

    names.append(name)
    coordinates.append(coordinate)
    geo_points.append(geo_point)

# Create a DataFrame for better readability
df = pd.DataFrame({
    'Name': names,
    'Coordinates': coordinates,
    'Geo Point': geo_points
})

# Print the DataFrame
print(df)
