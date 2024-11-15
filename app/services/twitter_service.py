import os
import tweepy

def fetch_tweets_for_token(token_name):
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
    consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
    consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    
    query = f"#{token_name}"
    tweets = api.search_tweets(q=query, lang="en", count=100)

    return [tweet.text for tweet in tweets]
