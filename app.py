import os
import yfinance as yf
from datetime import datetime, time, timedelta
from slack_bolt import App
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
load_dotenv()

SLACK_BOT_TOKEN = str(os.getenv('SLACK_BOT_TOKEN'))
SLACK_SIGNING_SECRET = str(os.getenv('SLACK_SIGNING_SECRET'))

def percent_change(start_point, end_point):
    return((float(end_point)-start_point)/abs(start_point))*100.00

def get_single_stock():
    # Hardcode as MSFT for now, need to catch error here, what if API fails?
    stock = yf.Ticker("MSFT")
    
    # General info
    long_name = stock.info['longName']
    symbol = stock.info['symbol']
    price = stock.info['regularMarketPrice']
    marketcap = stock.info['marketCap']
        
    
    # Week percent change:
    week_df = stock.history(period="5d")
    week_start_price = week_df.Open.iat[0]
    week_end_price = week_df.Open.iat[-1]
    week_percent_change = percent_change(week_start_price, week_end_price)    
    print(round(week_percent_change, 2))


get_single_stock()

# client = WebClient(SLACK_BOT_TOKEN)
# def get_convo_id():    
#     channel_name = "test-alerts"
#     convo_id = None
#     try:
#         for result in client.conversations_list():
#             if convo_id is not None:
#                 break
#             for channel in result["channels"]:
#                 if channel["name"] == channel_name:
#                     convo_id = channel["id"]                    
#                     return convo_id                    

#     except SlackApiError as e:
#         print(f"Error: {e}")

# def publish_message():
#     convo_id = get_convo_id()
#     try:    
#         result = client.chat_postMessage(
#             channel=convo_id,
#             text="Hello world!"
#         )
#         print(result)

#     except SlackApiError as e:
#         print(f"Error: {e}")


# Start Slack App
app = App(
    token=SLACK_BOT_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET
)

# Start Bolt app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))