import requests
from geocode_location import geocode_location

def get_weather(location, days=5):
    """
    Fetch weather data for a given location.
    Returns a dictionary with current weather and forecast data for the next `days` days.
    """
    try:
        WEATHER_API_KEY = ""
        lat, lon = geocode_location(location)
        # API call for both current weather and forecast data for the next 'days' days
        url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={lat},{lon}&days={days}&aqi=no"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()

            # Forecast Data for the next 'days' days
            forecast = []
            for day in data['forecast']['forecastday']:
                forecast.append({
                    "date": day['date'],
                    "temperature_max_c": day['day']['maxtemp_c'],
                    "temperature_min_c": day['day']['mintemp_c'],
                    "wind_kph": day['day']['maxwind_kph']
                })

            # Return the weather data in the desired format
            return {
                "location": f"{data['location']['name']}, {data['location']['country']}",
                "temperature_c": data['current']['temp_c'],
                "condition": data['current']['condition']['text'],
                "wind_kph": data['current']['wind_kph'],
                "forecast": forecast
            }
        else:
            return {"error": f"Weather data unavailable. Error: {response.status_code}"}

    except Exception as e:
        return {"error": f"Weather data unavailable. Error: {e}"}

# Test the function
if __name__ == "__main__":
    weather_data = get_weather("Stony Brook, New York")
    print(weather_data)
