import os
import tweepy
import json
import requests
from slack_bolt import App
from dotenv import load_dotenv
load_dotenv()

# Slack env variables:
SLACK_BOT_TOKEN = str(os.getenv('SLACK_BOT_TOKEN'))
SLACK_SIGNING_SECRET = str(os.getenv('SLACK_SIGNING_SECRET'))
WEBHOOK_URI = str(os.getenv('WEBHOOK_URI'))

# Twitter env variables:
TWITTER_API_KEY = str(os.getenv('TWITTER_API_KEY'))
TWITTER_API_SECRET = str(os.getenv('TWITTER_API_SECRET'))
TWITTER_ACCESS_TOKEN = str(os.getenv('TWITTER_ACCESS_TOKEN'))
TWITTER_ACCESS_TOKEN_SECRET = str(os.getenv('TWITTER_ACCESS_TOKEN_SECRET'))

slack_data = {'text': "Tweet sent!"}

# Start Twitter App
class CustomStreamListener(tweepy.StreamListener):

    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):        
        print(f"{tweet.user.name}:{tweet.text}")
        response = requests.post(
            WEBHOOK_URI, data=json.dumps(slack_data), 
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code != 200:
            raise ValueError(
                'Request to slack returned an error %s, the response is:\n%s'
                % (response.status_code, response.text)
            )

    def on_error(self, status):
        print("Error detected")

# Authenticate with Twitter
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

tweets_listener = CustomStreamListener(api)
stream = tweepy.Stream(api.auth, tweets_listener)
stream.filter(follow=["198899653"])
# stream.filter(track=["Javascript"], languages=["en"])

# Start Slack App
app = App(
    token=SLACK_BOT_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET
)

# Start Bolt app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))