import folium
import pandas as pd

# Sample data
data = pd.DataFrame({
    'IP': ['192.0.2.1', '198.51.100.2'],
    'Latitude': [37.7749, 40.7128],
    'Longitude': [-122.4194, -74.0060]
})

# Create a map centered on the average location
m = folium.Map(location=[data['Latitude'].mean(), data['Longitude'].mean()], zoom_start=4)

# Add markers
for _, row in data.iterrows():
    folium.Marker([row['Latitude'], row['Longitude']], popup=row['IP']).add_to(m)

# Save map to an HTML file
m.save('ip_geolocation_map.html')
