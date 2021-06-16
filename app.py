import os
from datetime import datetime, time, timedelta
from slack_bolt import App
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
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

def schedule_message():
    convo_id = get_convo_id()
    every_friday = datetime.now().astimezone()
    while every_friday.weekday() != 4:
        every_friday += timedelta(1)

    scheduled_time = time(hour=11, minute=30)
    scheduled_timestamp = datetime.combine(every_friday, scheduled_time).strftime('%s')
    
    try:
        result = client.chat_scheduleMessage(
            channel=convo_id,
            text="Publish future Friday message test!",
            post_at=scheduled_timestamp
        )
        print(result)
    except SlackApiError as e:
        print(f"Error: {e}")

schedule_message()

# Start Slack App
app = App(
    token=SLACK_BOT_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET
)

# Start Bolt app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))