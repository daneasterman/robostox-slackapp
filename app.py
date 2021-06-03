import os
from slack_bolt import App
from dotenv import load_dotenv

# Disable for now:
# from slack_bolt.adapter.flask import SlackRequestHandler
# from flask import Flask, request, Response

load_dotenv()

SLACK_BOT_TOKEN = str(os.getenv('SLACK_BOT_TOKEN'))
SLACK_SIGNING_SECRET = str(os.getenv('SLACK_SIGNING_SECRET'))
WEBHOOK_URI = str(os.getenv('WEBHOOK_URI'))

app = App(
    token=SLACK_BOT_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET
)

# Start Bolt app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))