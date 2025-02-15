""" 
[!] if you want to use this script, you have to go to https://ipinfo.io/signup and get your own API key  
[!] put the API token in line 47, and then you are good to go! 
"""

import requests
import ipaddress
import folium

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org')
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching public IP: {e}")
        return None

def get_geolocation(ip, api_token):
    url = f"https://ipinfo.io/{ip}/json"
    params = {'token': api_token} if api_token else {}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching geolocation data: {e}")
        return None

def generate_map(latitude, longitude, ip):
    """Generate a map using folium and save it as an HTML file."""
    m = folium.Map(location=[latitude, longitude], zoom_start=10)

    # Add a marker for the IP location
    folium.Marker(
        location=[latitude, longitude],
        popup=f"IP: {ip}",
        tooltip="Click for details"
    ).add_to(m)

    map_file = "ip_geolocation_map.html"
    m.save(map_file)
    print(f"\nMap saved to {map_file}. Open this file in your browser to view the map.")

def main():
    # Get your free API token from https://ipinfo.io/signup
    API_TOKEN = 'e5bc1b2a9e48db'  

    ip = input("Enter an IP address (press Enter to use your public IP): ").strip()

    if not ip:
        print("\nUsing public IP...")
        ip = get_public_ip()
        if not ip:
            print("Could not determine public IP.")
            return
    else:
        try:
            ip_obj = ipaddress.ip_address(ip)
            if ip_obj.is_private:
                print("Private IP addresses don't have geolocation data.")
                return
        except ValueError:
            print("Invalid IP address format.")
            return

    print(f"\nFetching geolocation data for {ip}...")
    data = get_geolocation(ip, API_TOKEN)

    if data:
        print("\nGeolocation Information:")
        print(f"IP Address: {data.get('ip', 'N/A')}")
        print(f"Hostname: {data.get('hostname', 'N/A')}")
        print(f"City: {data.get('city', 'N/A')}")
        print(f"Region: {data.get('region', 'N/A')}")
        print(f"Country: {data.get('country', 'N/A')}")
        print(f"Location: {data.get('loc', 'N/A')}")
        print(f"Organization: {data.get('org', 'N/A')}")
        print(f"Postal Code: {data.get('postal', 'N/A')}")
        print(f"Timezone: {data.get('timezone', 'N/A')}")

        if 'loc' in data:
            latitude, longitude = map(float, data['loc'].split(','))
            print(f"\nCoordinates: Latitude = {latitude}, Longitude = {longitude}")

            generate_map(latitude, longitude, ip)
        else:
            print("No location data available to generate a map.")
    else:
        print("Failed to retrieve geolocation data.")

if __name__ == "__main__":
    main()
