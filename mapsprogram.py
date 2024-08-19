import requests
import folium
import polyline

# Define the latitude and longitude coordinates for the locations
coordinates = [
    (80.499174, 16.494637),  # Corrected: Longitude, Latitude for location in India
    (80.504342, 16.485853),  # Corrected: Longitude, Latitude
    (80.511704, 16.465126),  # Corrected: Longitude, Latitude
    (80.527728, 16.516001)
]

# Create the coordinates string for the API request (lon,lat pairs)
coordinates_str = ";".join([f"{lon},{lat}" for lon, lat in coordinates])

# Specify the OSRM public server endpoint
osrm_url = f"http://router.project-osrm.org/route/v1/driving/{coordinates_str}?overview=full&geometries=polyline&steps=true"

# Send the request to the OSRM server
response = requests.get(osrm_url)

# Check if the request was successful
if response.status_code == 200:
    route = response.json()['routes'][0]
    distance = route['distance']
    duration = route['duration']
    polyline_points = route['geometry']

    # Decode the polyline to get the full route as a list of coordinates
    route_coordinates = polyline.decode(polyline_points)

    print(f"Total Distance: {distance / 1000} km")
    print(f"Total Duration: {duration / 60} minutes")

    # Create a Folium map centered around the first location
    m = folium.Map(location=[coordinates[0][1], coordinates[0][0]], zoom_start=6)

    # Add markers for each location
    for coord, name in zip(coordinates, ["New York", "Philadelphia", "Hartford", "Boston"]):
        folium.Marker(location=[coord[1], coord[0]], popup=name).add_to(m)

    # Add the shortest path as a PolyLine on the map
    folium.PolyLine(locations=route_coordinates, color="blue", weight=5, opacity=0.7).add_to(m)

    # Save the map to an HTML file
    m.save("map_with_route.html")

    # Optionally, display the map in a Jupyter Notebook
    m

else:
    print(f"Error: {response.status_code}")
