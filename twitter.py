import os
import tweepy
from dotenv import load_dotenv
load_dotenv()

TWITTER_API_KEY = str(os.getenv('TWITTER_API_KEY'))
TWITTER_API_SECRET = str(os.getenv('TWITTER_API_SECRET'))
TWITTER_ACCESS_TOKEN = str(os.getenv('TWITTER_ACCESS_TOKEN'))
TWITTER_ACCESS_TOKEN_SECRET = str(os.getenv('TWITTER_ACCESS_TOKEN_SECRET'))

class CustomStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        # make webhook post request here
        print(f"{tweet.user.name}:{tweet.text}")

    def on_error(self, status):
        print("Error detected")

# Authenticate with Twitter
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

tweets_listener = CustomStreamListener(api)
stream = tweepy.Stream(api.auth, tweets_listener)

# stream.filter(follow=["198899653"])
stream.filter(track=["Python"], languages=["en"])

