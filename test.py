import tweepy
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Twitter API v2 credentials
CLIENT_ID = os.getenv('TWITTER_CLIENT_ID')
CLIENT_SECRET = os.getenv('TWITTER_CLIENT_SECRET')
BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

def initialize_twitter_client():
    """Initialize and return Twitter API v2 client"""
    try:
        client = tweepy.Client(
            bearer_token=BEARER_TOKEN,
            consumer_key=CLIENT_ID,
            consumer_secret=CLIENT_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET
            
        )
        return client
    except Exception as e:
        print(f"Error initializing Twitter client: {e}")
        return None

def search_tweets(client, query, max_results=10):
    """Search for tweets using Twitter API v2"""
    try:
        # Search tweets
        tweets = client.search_recent_tweets(
            query=query,
            max_results=max_results,
            tweet_fields=['created_at', 'lang', 'public_metrics']
        )
        
        if tweets.data is not None:
            return tweets.data
        else:
            return []
            
    except Exception as e:
        print(f"Error searching tweets: {e}")
        return []

def get_user_info(client, username):
    """Get user information using Twitter API v2"""
    try:
        # Get user info
        user = client.get_user(username=username, user_fields=[
            'created_at',
            'description',
            'public_metrics'
        ])
        
        return user.data if user.data else None
        
    except Exception as e:
        print(f"Error getting user info: {e}")
        return None

def main():
    # Initialize Twitter client
    client = initialize_twitter_client()
    if not client:
        return
    
    # Example usage
    # 1. Search for tweets
    query = "python"
    tweets = search_tweets(client, query)
    print("\nRecent tweets about Python:")
    for tweet in tweets:
        print(f"- {tweet.text}")
    
    # 2. Get user information
    username = "TwitterDev"
    user = get_user_info(client, username)
    if user:
        print(f"\nUser information for @{username}:")
        print(f"Description: {user.description}")
        print(f"Followers: {user.public_metrics['followers_count']}")
        print(f"Following: {user.public_metrics['following_count']}")

if __name__ == "__main__":
    main()