import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud

# Set page config to wide mode
st.set_page_config(page_title="Localized Market Intelligence Tool", page_icon="📊", layout="wide")

# Inject custom CSS for full-width layout
st.markdown(
    """
    <style>
    .main > div {
        max-width: 100%;
        padding-left: 5%;
        padding-right: 5%;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar for user inputs
st.sidebar.header('User Input')
location = st.sidebar.text_input('Enter your location (e.g., Stony Brook, New York):')
vertical = st.sidebar.selectbox(
    'Select a vertical:', 
    ['auto', 'real estate', 'retail', 'sports', 'other', 'finance', 'healthcare', 'technology', 'entertainment', 'education', 'travel', 'food & beverage']
)

# Fetch Data Button
if st.sidebar.button('Fetch Data'):
    if location and vertical:
        with st.spinner("Fetching data..."):  # Show a loading spinner
            payload = {"location": location, "vertical": vertical}
            response = requests.post("http://localhost:5000/get_data", json=payload)
            if response.status_code == 200:
                st.session_state.data = response.json()
                st.success("Data fetched successfully!")  # Show success message
            else:
                st.error("Failed to fetch data from the backend.")
    else:
        st.warning("Please enter both a location and a vertical.")

# Reset Button to clear session state
if st.sidebar.button('Reset'):
    if 'data' in st.session_state:
        del st.session_state.data
    st.success("Session state cleared. You can fetch new data.")

# Title in the center
st.markdown("<h1 style='text-align: center;'>🌍 Localized Market Intelligence Tool</h1>", unsafe_allow_html=True)

# Display data if available in session state
if 'data' in st.session_state:
    data = st.session_state.data

    # Row 1: Weather and News/Events
    st.subheader('Welcome to: ' + location + '!')
    col1, col2 = st.columns(2)
    with col1:
        # Weather Section
        # Weather Section
        st.subheader('🌦 Weather')
        if isinstance(data["weather"], dict) and "error" not in data["weather"]:
            # Create a compact and visually appealing layout for current weather
            col1_1, col1_2, col1_3 = st.columns(3)
            with col1_1:
                st.write("**🌡️ Temperature**")
                st.write(f"{data['weather']['temperature_c']}°C")
            with col1_2:
                st.write("**🌤️ Condition**")
                st.write(data['weather']['condition'])
            with col1_3:
                st.write("**💨 Wind Speed**")
                st.write(f"{data['weather']['wind_kph']} km/h")

            # Add a small divider for better separation
           

            # Display the forecast data in a line chart
            forecast_table = pd.DataFrame(data["weather"]["forecast"])
            fig = px.line(
                forecast_table,
                x="date",
                y=["temperature_max_c", "temperature_min_c", "wind_kph"],
                labels={"value": "Temperature (°C) / Wind (Km/h)", "date": "Date"},
                title="Temperature and Wind Forecast",
                color_discrete_map={"temperature_max_c": "red", "temperature_min_c": "blue", "wind_kph": "green"}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error(data["weather"].get("error", "No weather data available."))

    with col2:
        # News/Events Section
        st.subheader('📰 News & 🎭 Events')
        tab1, tab2 = st.tabs(["News", "Events"])
        with tab1:
            if isinstance(data["news"], list):
                news_table = pd.DataFrame([{
                    "Title": article["title"],
                    "Source": f'<a href="{article["url"]}" target="_blank">{article["source"]}</a>'
                } for article in data["news"]])
                st.markdown(news_table.to_html(escape=False), unsafe_allow_html=True)
            else:
                st.error(data["news"].get("error", "No news data available."))
        with tab2:
            if isinstance(data["events"], list):
                events_table = pd.DataFrame([{
                    "Event Name": event["event"],
                    "Date": event["date"],
                    "Venue": event["venue"],
                    "More Info": f'<a href="{event["url"]}" target="_blank">Ticketmaster</a>'
                } for event in data["events"]])
                st.markdown(events_table.to_html(escape=False), unsafe_allow_html=True)
            else:
                st.error(data["events"].get("error", "No events data available."))

    st.markdown("---")  # Horizontal line for separation

    # Row 2: Traffic, Sentiment, and Word Cloud
    st.subheader('Insights & Analysis')
    col1, col2, col3 = st.columns([2, 2, 1])  # Adjust column widths
    with col1:
        # Traffic Section
        st.subheader('🚦 Traffic Insights')
        if isinstance(data["traffic"], dict) and "traffic_info" in data["traffic"]:
            traffic_df = pd.DataFrame(data["traffic"]["traffic_info"])
            
            # Bar Chart for Traffic Delays
            st.write("**Traffic Delays by Destination**")
            fig = px.bar(
                traffic_df,
                x="destination",
                y="traffic_delay_min",
                labels={"destination": "Destination", "traffic_delay_min": "Traffic Delay (minutes)"},
                color="traffic_delay_min",
                color_continuous_scale="Viridis"
            )
            st.plotly_chart(fig, use_container_width=True)

            # Display the average traffic delay
            st.write(f"**Average Traffic Delay:** {data['traffic']['average_delay_min']:.2f} minutes")
        else:
            st.error(data["traffic"].get("error", "No traffic data available."))

    with col2:
        # Sentiment Distribution Section
        st.subheader('📈 Sentiment Distribution')
        if isinstance(data["sentiment"], dict) and "error" not in data["sentiment"]:
            if "sentiment_distribution" in data["sentiment"]:
                sentiment_distribution = data["sentiment"]["sentiment_distribution"]
                sentiment_distribution_df = pd.DataFrame(list(sentiment_distribution.items()), columns=["Sentiment", "Count"])
                
                fig = px.bar(
                    sentiment_distribution_df,
                    x="Sentiment",
                    y="Count",
                    labels={"Sentiment": "Sentiment Category", "Count": "Number of Posts"},
                    color="Sentiment",
                    color_continuous_scale="Blues"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No sentiment distribution data available for histogram.")
        else:
            st.error(data["sentiment"].get("error", "No sentiment data available."))

    with col3:
        # Word Cloud Section
        st.subheader('☁️ Word Cloud')
        if isinstance(data["sentiment"], dict) and "error" not in data["sentiment"]:
            if "trendy_words" in data["sentiment"]:
                trendy_words = data["sentiment"]["trendy_words"]

                # Create a figure and axis for the word cloud
                fig, ax = plt.subplots(figsize=(5, 3))

                # Plot words with varying sizes based on frequency
                x, y = 0.1, 0.9  # Starting position for the first word
                for word, freq in trendy_words.items():
                    ax.text(
                        x, y,
                        word,
                        fontsize=10 + freq * 2,  # Adjust font size based on frequency
                        ha='center', va='center',
                        color='blue'  # You can customize the color
                    )
                    x += 0.2  # Move to the next position
                    if x > 0.9:  # Move to the next line if the current line is full
                        x = 0.1
                        y -= 0.2

                # Remove axes and borders
                ax.axis('off')

                # Display the plot in Streamlit
                st.pyplot(fig)
            else:
                st.warning("No trendy words data available for word cloud.")
        else:
            st.error(data["sentiment"].get("error", "No sentiment data available."))

    st.markdown("---")  # Horizontal line for separation

    # Row 3: Advertiser Summary
    st.subheader('📊 Advertiser Summary')
    st.write(data["advertiser_summary"])