from get_weather_info import get_weather
from get_news_info import get_news
from get_events_info import get_events
from get_traffic_info import get_traffic
from get_sentiment_info import get_sentiment
from llm_response import generate_prompt
from llm_response import generate_advertiser_summary

# Test location
location = "Stony Brook, New York"

# Test weather
print("🌦 Testing Weather Module 🌦")
weather_data = get_weather(location)
print(weather_data)
print("-" * 40)

# Test news
print("📰 Testing News Module 📰")
news_data = get_news(location)
print(news_data)
print("-" * 40)

# Test events
print("🎭 Testing Events Module 🎭")
event_data = get_events(location)
print(event_data)
print("-" * 40)

# Test traffic
print("🚦 Testing Traffic Module 🚦")
traffic_data = get_traffic(location)
print(traffic_data)
print("-" * 40)

# Test sentiment
print("📊 Testing Sentiment Module 📊")
sentiment_data = get_sentiment(location)
print(sentiment_data)
print("-" * 40)


# Test LLM response
print("🤖 Testing LLM Response 🤖")
prompt = generate_prompt(weather_data, news_data, event_data, traffic_data, sentiment_data, "travel")
summary = generate_advertiser_summary(prompt)
print(summary)