from flask import Flask, jsonify, request
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from get_weather_info import get_weather
from get_news_info import get_news
from get_events_info import get_events
from get_traffic_info import get_traffic
from get_sentiment_info import get_sentiment
from llm_response import generate_prompt
from llm_response import generate_advertiser_summary


app = Flask(__name__)

# Load GPT-2 model and tokenizer
# tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
# model = GPT2LMHeadModel.from_pretrained("gpt2")


@app.route('/get_data', methods=['POST'])
def get_data():
    # Get location and vertical from the request
    location = request.json.get('location')
    vertical = request.json.get('vertical')

    if not location or not vertical:
        return jsonify({"error": "Location and vertical are required."}), 400

    try:
        # Fetch data from all modules
        weather_data = get_weather(location)
        news_data = get_news(location)
        event_data = get_events(location)
        traffic_data = get_traffic(location)
        sentiment_data = get_sentiment(location)

        # Generate advertiser summary using GPT-2
        prompt = generate_prompt(weather_data, news_data, event_data, traffic_data, sentiment_data, vertical)
        summary = generate_advertiser_summary(prompt)

        # Return the data and summary as JSON
        return jsonify({
            "weather": weather_data,
            "news": news_data,
            "events": event_data,
            "traffic": traffic_data,
            "sentiment": sentiment_data,
            "advertiser_summary": summary
        })
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)