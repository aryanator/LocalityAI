import streamlit as st
import requests
import pandas as pd

# Streamlit UI
st.title('Localized Market Intelligence Tool')

# User Input
location = st.text_input('Enter your location (e.g., Stony Brook, New York):')
vertical = st.selectbox('Select a vertical:', ['auto', 'real estate', 'retail', 'other'])

if st.button('Fetch Data'):
    if location and vertical:
        # Prepare payload for the backend
        payload = {
            "location": location,
            "vertical": vertical
        }

        # Send request to backend
        response = requests.post("http://localhost:5000/get_data", json=payload)

        if response.status_code == 200:
            data = response.json()

            # Display Weather Data
            st.subheader('🌦 Weather')
            if isinstance(data["weather"], dict) and "error" not in data["weather"]:
                weather_table = pd.DataFrame([{
                    "Location": data["weather"]["location"],
                    "Temperature (°C)": data["weather"]["temperature_c"],
                    "Condition": data["weather"]["condition"],
                    "Wind Speed (km/h)": data["weather"]["wind_kph"]
                }])
                st.table(weather_table)
            else:
                st.error(data["weather"].get("error", "No weather data available."))

            # Display News Data
            st.subheader('📰 News')
            if isinstance(data["news"], list):
                news_table = pd.DataFrame([{
                    "Title": article["title"],
                    "Source": f'[🔗 {article["source"]}]({article["url"]})'
                } for article in data["news"]])
                st.markdown(news_table.to_markdown(index=False), unsafe_allow_html=True)
            else:
                st.error(data["news"].get("error", "No news data available."))

            # Display Events Data
            st.subheader('🎭 Events')
            if isinstance(data["events"], list):
                events_table = pd.DataFrame([{
                    "Event Name": event["event"],
                    "Date": event["date"],
                    "Venue": event["venue"],
                    "More Info": f'[🔗 Ticketmaster]({event["url"]})'
                } for event in data["events"]])
                st.markdown(events_table.to_markdown(index=False), unsafe_allow_html=True)
            else:
                st.error(data["events"].get("error", "No events data available."))

            # Display Traffic Data
            st.subheader('🚦 Traffic')
            if isinstance(data["traffic"], dict) and "traffic_info" in data["traffic"]:
                # Create a DataFrame for the traffic information
                traffic_table = pd.DataFrame([{
                    "Destination": info["destination"],
                    "Distance (km)": f'{info["distance_km"]:.2f}',
                    "Duration (with traffic)": f'{info["duration_with_traffic_min"]:.2f} min',
                    "Duration (without traffic)": f'{info["duration_without_traffic_min"]:.2f} min',
                    "Traffic Delay": f'{info["traffic_delay_min"]:.2f} min'
                } for info in data["traffic"]["traffic_info"]])
                
                # Display the table
                st.table(traffic_table)
                
                # Display the average traffic delay
                st.write(f"**Average Traffic Delay:** {data['traffic']['average_delay_min']:.2f} minutes")
            else:
                st.error(data["traffic"].get("error", "No traffic data available."))

            # Display Sentiment Analysis
            st.subheader('📈 Sentiment Analysis')   
            if isinstance(data["sentiment"], dict) and "error" not in data["sentiment"]:
                sentiment_table = pd.DataFrame([{
                    "Entity": entity,
                    "Sentiment": sentiment
                } for entity, sentiment in data["sentiment"].items()])
                st.table(sentiment_table)
            else:
                st.error(data["sentiment"].get("error", "No sentiment data available."))

            # Display Advertiser Summary
            st.subheader('📊 Advertiser Summary')
            st.write(data["advertiser_summary"])

        else:
            st.error("Failed to fetch data from the backend.")
    else:
        st.warning("Please enter both a location and a vertical.")