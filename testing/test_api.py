import requests

# 🚨 Replace these with your actual API keys after signing up
WEATHER_API_KEY = "0a6a8b4f038241d78a8160949251303"  # Update with your WeatherAPI key
NEWS_API_KEY = "059619af30b749a1909419ab5cbf1fb8"
TICKETMASTER_API_KEY = "QbdotTtS7bK3U7r6nwi1Qp3e9g241GBS"  # Updated to Ticketmaster API key
TRAFFIC_API_KEY = "5acRBgJ6yO9HundfNEBt9EBYdS232PDiIjsvcMrc_k4"
TWITTER_BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAOVZywEAAAAA%2BvYeh%2FdRFTas9MeBVGoeDQ9%2Fuvs%3Dt2u6bQtQiCG315ORgn7IA3WBZfFY2KQ1UuU0LhdD3dyRrd8O86"

# Sample location (Modify as needed)
CITY = "New York"
ZIPCODE = "10001"
STATE = "NY"
COUNTRY = "US"
LAT, LON = 40.7128, -74.0060  # Coordinates for NYC

# 1️⃣ **Weather API (WeatherAPI)**
def test_weather():
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={CITY}&aqi=no"
    response = requests.get(url)
    print("\n🌦 Weather Data:", response.json())

# 2️⃣ **News API (NewsAPI)**
def test_news():
    url = f"https://newsapi.org/v2/top-headlines?country=us&category=general&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    print("\n📰 News Data:", response.json())

# 3️⃣ **Events API (Ticketmaster Discovery API)**
def test_events():
    # Ticketmaster API endpoint
    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    
    # Query parameters
    params = {
        "apikey": TICKETMASTER_API_KEY,
        "city": CITY,
        "countryCode": COUNTRY,
        "size": 5  # Number of events to fetch (optional)
    }
    
    # Make the request
    response = requests.get(url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        events = data.get("_embedded", {}).get("events", [])
        
        if events:
            print("\n🎭 Events Data:")
            for event in events:
                print(f"Event: {event['name']}")
                print(f"Date: {event['dates']['start']['localDate']}")
                print(f"Venue: {event['_embedded']['venues'][0]['name']}")
                print(f"URL: {event['url']}")
                print("-" * 40)
        else:
            print("\n🎭 No events found.")
    else:
        print(f"\n🎭 Events Data Error: {response.status_code} - {response.json()}")

# 4️⃣ **Traffic API (HERE Traffic)**
def test_traffic():
    url = f"https://traffic.api.here.com/traffic/6.3/flow.json?prox={LAT},{LON},5000&apiKey={TRAFFIC_API_KEY}"
    response = requests.get(url)
    print("\n🚦 Traffic Data:", response.json())

# 5️⃣ **Trending Hashtags (Twitter API)**
def test_twitter():
    url = "https://api.twitter.com/2/tweets/search/recent?query=trending&max_results=5"
    headers = {"Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"}
    response = requests.get(url, headers=headers)
    print("\n📢 Twitter Trends:", response.json())

# **Run all tests**
if __name__ == "__main__":
    test_weather()
    test_news()
    test_events()
    test_traffic()
    test_twitter()