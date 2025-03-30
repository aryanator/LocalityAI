import requests
from geocode_location import geocode_location

def get_traffic(location):
    """
    Fetch traffic data for a given location.
    Returns a dictionary with traffic information or an error message.
    """
    try:
        HERE_API_KEY = "Replace with your API Key"  # Replace with your HERE API key
        
        # Step 1: Get coordinates for the location
        lat, lon = geocode_location(location)
        origin = f"{lat},{lon}"  # Convert to "lat,lon" format
        print(f"Coordinates for {location}: {origin}")  # Debug print

        # Step 2: Find nearby hotspots using HERE Places API
        places_url = "https://discover.search.hereapi.com/v1/discover"
        categories = {
            "restaurant": "restaurant",
            "gas_station": "gas-station",
            "university": "university",
            "shopping_mall": "shopping-mall",
            "hospital": "hospital"
        }
        
        hotspots = []
        for category_name, category_id in categories.items():
            params = {
                "at": f"{lat},{lon}",
                "q": category_name,
                "apiKey": HERE_API_KEY,
                "limit": 1  # Fetch 1 result per category
            }
            response = requests.get(places_url, params=params)
            if response.status_code == 200:
                data = response.json()
                if "items" in data and len(data["items"]) > 0:
                    place = data["items"][0]
                    hotspots.append({
                        "name": place["title"],
                        "location": f"{place['position']['lat']},{place['position']['lng']}"
                    })
                    print(f"Found {category_name}: {place['title']} at {place['position']['lat']},{place['position']['lng']}")  # Debug print
                else:
                    print(f"No {category_name} found near {location}")  # Debug print
            else:
                print(f"HERE Places API Error for {category_name}: {response.status_code} - {response.text}")  # Debug print

        # Step 3: Calculate traffic trends for each hotspot
        total_delay = 0
        traffic_info = []
        for hotspot in hotspots:
            url = "https://router.hereapi.com/v8/routes"
            params = {
                "transportMode": "car",
                "origin": origin,
                "destination": hotspot["location"],
                "return": "summary",
                "apikey": HERE_API_KEY
            }
            response = requests.get(url, params=params)
            print(f"Traffic API Response for {hotspot['name']}: {response.status_code}")  # Debug print
            
            if response.status_code == 200:
                data = response.json()
                print(f"Traffic API Data for {hotspot['name']}: {data}")  # Debug print
                
                if "routes" in data and len(data["routes"]) > 0:
                    route = data["routes"][0]
                    summary = route["sections"][0]["summary"]
                    delay = (summary["duration"] - summary["baseDuration"]) / 60  # Delay in minutes
                    total_delay += delay
                    traffic_info.append({
                        "destination": hotspot["name"],
                        "distance_km": summary["length"] / 1000,
                        "duration_with_traffic_min": summary["duration"] / 60,
                        "duration_without_traffic_min": summary["baseDuration"] / 60,
                        "traffic_delay_min": delay
                    })
                else:
                    print(f"No routes found for destination: {hotspot['name']}")  # Debug print
            else:
                print(f"Traffic API Error for {hotspot['name']}: {response.status_code} - {response.text}")  # Debug print
        
        avg_delay = total_delay / len(hotspots) if hotspots else 0
        return {
            "traffic_info": traffic_info,
            "average_delay_min": avg_delay
        }
    except Exception as e:
        return {"error": f"Traffic data unavailable. Error: {e}"}

# Test the function
if __name__ == "__main__":
    traffic_data = get_traffic("San Francisco, California")
    
    # Print the traffic data in a clean and organized way
    if "error" in traffic_data:
        print(f"🚦 Error: {traffic_data['error']}")
    else:
        print("\n🚦 Traffic Information:")
        for info in traffic_data["traffic_info"]:
            print(f"Destination: {info['destination']}")
            print(f"  Distance: {info['distance_km']:.2f} km")
            print(f"  Duration (with traffic): {info['duration_with_traffic_min']:.2f} minutes")
            print(f"  Duration (without traffic): {info['duration_without_traffic_min']:.2f} minutes")
            print(f"  Traffic Delay: {info['traffic_delay_min']:.2f} minutes")
            print("-" * 40)
        print(f"Average Traffic Delay: {traffic_data['average_delay_min']:.2f} minutes")
