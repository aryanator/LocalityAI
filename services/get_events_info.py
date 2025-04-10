import requests
from geocode_location import geocode_location

def get_events(location, num_events=5):
    """
    Fetch event data for a given location.
    Returns a list of events or an error message.
    """
    try:
        TICKETMASTER_API_KEY = "QbdotTtS7bK3U7r6nwi1Qp3e9g241GBS"
        lat, lon = geocode_location(location)
        url = "https://app.ticketmaster.com/discovery/v2/events.json"
        params = {
            "apikey": TICKETMASTER_API_KEY,
            "latlong": f"{lat},{lon}",
            "radius": 50,  # Search within 50 km
            "size": num_events  # Fetch up to `num_events`
        }
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            events = data.get("_embedded", {}).get("events", [])
            if events:
                # Return a list of events (up to `num_events`)
                return [
                    {
                        "event": event["name"],
                        "date": event["dates"]["start"]["localDate"],
                        "venue": event["_embedded"]["venues"][0]["name"],
                        "url": event["url"]
                    }
                    for event in events[:num_events]  # Limit to `num_events`
                ]
            else:
                return {"error": "No events found."}
        else:
            return {"error": f"Event data unavailable. Error: {response.status_code}"}
    except Exception as e:
        return {"error": f"Event data unavailable. Error: {e}"}

# Test the function
if __name__ == "__main__":
    event_data = get_events("Stony Brook, New York", num_events=15)
    print(event_data)