import os
import yfinance as yf
from numerize import numerize
from datetime import datetime, time, timedelta
from slack_bolt import App
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from generate_stock import render_stock_content
from dotenv import load_dotenv
load_dotenv()

SLACK_BOT_TOKEN = str(os.getenv('SLACK_BOT_TOKEN'))
SLACK_SIGNING_SECRET = str(os.getenv('SLACK_SIGNING_SECRET'))

client = WebClient(SLACK_BOT_TOKEN)
def get_convo_id():
    channel_name = "test-alerts"
    convo_id = None
    try:
        for result in client.conversations_list():
            if convo_id is not None:
                break
            for channel in result["channels"]:
                if channel["name"] == channel_name:
                    convo_id = channel["id"]                    
                    return convo_id                    

    except SlackApiError as e:
        print(f"Error: {e}")

def publish_message():
    convo_id = get_convo_id()
    content = render_stock_content()
    try:    
        result = client.chat_postMessage(
            channel=convo_id,
            blocks=content
        )
        print(result)

    except SlackApiError as e:
        print(f"Error: {e}")

# Need to call function:
publish_message()

# Start Slack App
app = App(
    token=SLACK_BOT_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET
)

# Start Bolt app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))