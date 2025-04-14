import requests

def get_news(location, num_articles=5):
    """
    Fetch news data for a given location.
    Returns a list of news articles or an error message.
    """
    try:
        NEWS_API_KEY = ""
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])
            if articles:
                # Return a list of articles (up to `num_articles`)
                return [
                    {
                        "title": article["title"],
                        "source": article["source"]["name"],
                        "url": article["url"]
                    }
                    for article in articles[:num_articles]  # Limit to `num_articles`
                ]
            else:
                return {"error": "No news articles found."}
        else:
            return {"error": f"News data unavailable. Error: {response.status_code}"}
    except Exception as e:
        return {"error": f"News data unavailable. Error: {e}"}

# Test the function
if __name__ == "__main__":
    news_data = get_news("Stony Brook, New York", num_articles=5)
    print(news_data)
