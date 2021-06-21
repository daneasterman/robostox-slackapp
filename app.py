import os
import yfinance as yf
from numerize import numerize
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

def get_period_percent_change(stock, period):
    df_period = stock.history(period=period)
    period_start = df_period.Open.iat[0]
    period_end = df_period.Open.iat[-1]
    period_percent_change = percent_change(period_start, period_end)
    return period_percent_change

def get_single_stock():
    # Hardcode as MSFT for now, need to catch error here, what if API fails?
    stock = yf.Ticker("MSFT")

    previous_close = stock.info['previousClose']
    current_price = stock.info['regularMarketPrice']
    raw_marketcap = stock.info['marketCap']
    marketcap = numerize.numerize(raw_marketcap, 2)   

    stock_data = {
        'symbol': stock.info['symbol'],
        'long_name': stock.info['longName'],
        'logo': stock.info['logo_url'],
        'current_price': current_price,
        'marketcap': marketcap,
        'day_percent_change': round(percent_change(previous_close, current_price), 2),
        'week_percent_change': round(get_period_percent_change(stock, "5d"), 2),
        'month_percent_change': round(get_period_percent_change(stock, "1mo"), 2),
        'year_percent_change': round(get_period_percent_change(stock, "ytd"), 2)
    }

    return stock_data
        

# stock_data = get_single_stock()

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
    try:    
        result = client.chat_postMessage(
            channel=convo_id,
            text="Test publish message function"
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