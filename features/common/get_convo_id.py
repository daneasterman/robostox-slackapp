import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
SLACK_BOT_TOKEN = str(os.getenv('SLACK_BOT_TOKEN'))
client = WebClient(SLACK_BOT_TOKEN)

def get_convo_id(channel_name):    
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