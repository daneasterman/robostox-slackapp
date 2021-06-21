import os
import tweepy
from dotenv import load_dotenv
from slack_sdk.webhook import WebhookClient
from slack_bolt import App
load_dotenv()

SLACK_BOT_TOKEN = str(os.getenv('SLACK_BOT_TOKEN'))
SLACK_SIGNING_SECRET = str(os.getenv('SLACK_SIGNING_SECRET'))
SLACK_WEBHOOK_URI = str(os.getenv('SLACK_WEBHOOK_URI'))

TWITTER_API_KEY = str(os.getenv('TWITTER_API_KEY'))
TWITTER_API_SECRET = str(os.getenv('TWITTER_API_SECRET'))
TWITTER_ACCESS_TOKEN = str(os.getenv('TWITTER_ACCESS_TOKEN'))
TWITTER_ACCESS_TOKEN_SECRET = str(os.getenv('TWITTER_ACCESS_TOKEN_SECRET'))

class CustomStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):        
        print(f"{tweet.user.name}: {tweet.text}")
        webhook = WebhookClient(SLACK_WEBHOOK_URI)        
        response = webhook.send(
            text=f"Twitter user: {tweet.user.name} just tweeted: {tweet.text}",
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "This is a mrkdwn section block :ghost: *this is bold*, and ~this is crossed out~, and <https://google.com|this is a link>"
                    }
                }
            ]
        )
        assert response.status_code == 200
        assert response.body == "ok"

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



