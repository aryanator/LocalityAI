import requests
import os
from together import Together


def generate_prompt(weather_data, news_data, event_data, traffic_data, sentiment_data, vertical):
    # Load GPT-2 model and tokenizer
    # tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    # model = GPT2LMHeadModel.from_pretrained("gpt2")

    # # Set the pad token ID to the eos token ID
    # tokenizer.pad_token_id = tokenizer.eos_token_id

    # Construct the prompt for GPT-2
    prompt = f"Generate an advertiser-focused summary for the following location and vertical:\n\n"

    # Add location and vertical to the prompt
    prompt += f"Location: {weather_data.get('location', 'N/A')}\nVertical: {vertical}\n\n"

    # Add weather data to the prompt
    prompt += f"Weather:\n"
    prompt += f"- Temperature: {weather_data.get('temperature_c', 'N/A')}°C\n"
    prompt += f"- Condition: {weather_data.get('condition', 'N/A')}\n"
    prompt += f"- Wind Speed: {weather_data.get('wind_kph', 'N/A')} kph\n"

    # Add news data to the prompt (only titles)
    prompt += f"\nNews:\n"
    if isinstance(news_data, list):
        for news in news_data[:3]:  # Limit to top 3 news articles
            prompt += f"- {news.get('title', 'N/A')}\n"
    else:
        prompt += "- No news data available.\n"

    # Add events data to the prompt (only titles and dates)
    prompt += f"\nEvents:\n"
    if isinstance(event_data, list):
        for event in event_data[:3]:  # Limit to top 3 events
            prompt += f"- {event.get('event', 'N/A')} ({event.get('date', 'N/A')})\n"
    else:
        prompt += "- No events data available.\n"

    # Add traffic data to the prompt (busiest and least busy areas)
    prompt += f"\nTraffic:\n"
    if isinstance(traffic_data, dict) and "traffic_info" in traffic_data:
        traffic_info = traffic_data["traffic_info"]
        if traffic_info:
            # Find the busiest and least busy areas
            busiest = max(traffic_info, key=lambda x: x.get("traffic_delay_min", 0))
            least_busy = min(traffic_info, key=lambda x: x.get("traffic_delay_min", 0))
            prompt += (
                f"- Busiest Area: {busiest.get('destination', 'N/A')} ({busiest.get('traffic_delay_min', 'N/A'):.2f} minutes delay)\n"
                f"- Least Busy Area: {least_busy.get('destination', 'N/A')} ({least_busy.get('traffic_delay_min', 'N/A'):.2f} minutes delay)\n"
            )
        else:
            prompt += "- No traffic data available.\n"
    else:
        prompt += "- No traffic data available.\n"


    # Add sentiment analysis to the prompt
    prompt += f"\nSentiment Analysis:\n"
    if isinstance(sentiment_data, dict) and "avg_sentiment" in sentiment_data:
        sentiment_score = sentiment_data["avg_sentiment"]
        sentiment_distribution = sentiment_data["sentiment_distribution"]
        prompt += f"- Sentiment Score: {sentiment_score:.2f}\n"
        prompt += f"- Sentiment Distribution: {sentiment_distribution}\n"

    else:
        prompt += "- No sentiment analysis available.\n"

    return prompt

def generate_advertiser_summary(prompt):
    # Set your API key as an environment variable (replace with your key)
    os.environ["TOGETHER_API_KEY"] = ""  

    # Initialize the client with the API key
    client = Together(api_key=os.environ["TOGETHER_API_KEY"])

    # Make a request to the model
    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400,
        temperature=0.7,
        top_p=0.7,
        top_k=50,
        repetition_penalty=1,
        stop=["<|eot_id|>", "<|eom_id|>"],
        stream=True
    )

    # Initialize a variable to accumulate the content
    result = ""

    # Process and accumulate the results
    for token in response:
        if hasattr(token, 'choices'):
            result += token.choices[0].delta.content

    # Return the accumulated result
    return result
