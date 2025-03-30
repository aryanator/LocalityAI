import praw
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from geocode_location import geocode_location
from collections import Counter
import re

# Reddit API credentials
REDDIT_CLIENT_ID = "Replace with your API Key"
REDDIT_CLIENT_SECRET = "Replace with your API Key"
USER_AGENT = "Replace with your API Key"

# Initialize Reddit API
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=USER_AGENT
)

def clean_text(text):
    """ Remove special characters, links, and unnecessary symbols from text. """
    text = re.sub(r"http\S+|www\S+|https\S+", '', text)  # Remove links
    text = re.sub(r'\W+', ' ', text)  # Remove non-alphabetic characters
    return text.lower()

def get_sentiment(location):
    """
    Fetch sentiment for a location using Reddit posts.
    Also extracts word frequency for a word cloud and sentiment distribution.
    """
    try:
        lat, lon = geocode_location(location)  # Get location coordinates

        # Search Reddit for location-based discussions
        search_results = reddit.subreddit("all").search(location, limit=100)

        posts = [post.title for post in search_results]
        if not posts:
            return {"error": "No relevant Reddit posts found for sentiment analysis."}

        # Perform sentiment analysis
        analyzer = SentimentIntensityAnalyzer()
        sentiment_scores = [analyzer.polarity_scores(post)["compound"] for post in posts]

        # Categorize sentiment into bins for distribution
        sentiment_distribution = {
            "very_positive": sum(1 for s in sentiment_scores if s > 0.6),
            "positive": sum(1 for s in sentiment_scores if 0.1 < s <= 0.6),
            "neutral": sum(1 for s in sentiment_scores if -0.1 <= s <= 0.1),
            "negative": sum(1 for s in sentiment_scores if -0.6 <= s < -0.1),
            "very_negative": sum(1 for s in sentiment_scores if s < -0.6)
        }

        # Extract trendy words for a word cloud
        all_words = ' '.join(clean_text(post) for post in posts).split()
        common_words = Counter(all_words).most_common(50)  # Top 50 frequent words

        return {
            "location": location,
            "avg_sentiment": sum(sentiment_scores) / len(sentiment_scores),
            "sentiment_distribution": sentiment_distribution,
            "trendy_words": dict(common_words),  # Returns word frequency for visualization
            "num_posts_analyzed": len(posts)
        }
    except Exception as e:
        return {"error": f"Sentiment analysis failed. Error: {e}"}

# Test the function
if __name__ == "__main__":
    sentiment_data = get_sentiment("Stony Brook, New York")
    print(sentiment_data)
