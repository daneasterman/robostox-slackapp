import os
import json
import yfinance as yf
from datetime import datetime, time, timedelta
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from flask import Flask, request, jsonify
from whitenoise import WhiteNoise

from generate_single import generate_stock_info, get_period_percent_change
from generate_multiple import get_multiple_stocks

from python_data.menus import multi_internal_select
from python_data.app_errors import plain_api_error, rich_api_error, generic_error_text

from dotenv import load_dotenv
load_dotenv()

# Heroku automatically pulls the variables from this:
SLACK_BOT_TOKEN = str(os.getenv('SLACK_BOT_TOKEN'))
SLACK_SIGNING_SECRET = str(os.getenv('SLACK_SIGNING_SECRET'))

# Start Slack App
app = App(
		token=SLACK_BOT_TOKEN,
		signing_secret=SLACK_SIGNING_SECRET
)

@app.event("app_home_opened")
def update_home_tab(client, event, logger):
  try:    
    client.views_publish(      
      user_id=event["user"],
      view={
        "type": "home",
        "callback_id": "home_view",
				"blocks": multi_internal_select
      }
    )  
  except Exception as e:
    logger.error(f"HOME TAB ERROR: {e}")

@app.action("ticker_select")
def ack_ticker_select(ack, action):	
	ack()
	tickers = []
	stocks_list =[]
	selected_options = action['selected_options']
	for s in selected_options:
		tickers.append(s['value'])
	for t in tickers:
		stock = yf.Ticker(t)
		week_change = round(get_period_percent_change(stock, "5d"), 2)
		# TO DO FORCE 0 HERE
		stock_dict = {
			'long_name': stock.info['longName'],
			'week_change': None if week_change == 0 else week_change
			}
		stocks_list.append(stock_dict)	
	publish_message(stocks_list)

def natural_lang(percent):
	if percent > 0:
		return "up"
	elif percent < 0:
		return "down"
	elif percent == 0:
		return "is unchanged"

client = WebClient(SLACK_BOT_TOKEN)
def publish_message(stocks_list):
	convo_id = get_convo_id()

	blocks = []
	intro = {
		"type": "section",
		"text": {
			"type": "mrkdwn",
			"text": "*Happy Friday!*  :tada:  Here's your weekly portfolio update:"
		}
	}
	blocks.append(intro)
	top_divider = {"type": "divider"}
	blocks.append(top_divider)

	for s in stocks_list:		
		main_info = {
			"type": "section",
			"text": {
				"type": "mrkdwn",			
				"text": f"*{s['long_name']}* is trading at `blah` and {natural_lang(s['week_change'])} {s['week_change']} for the week."
			},
		}		
		blocks.append(main_info)
	
	bottom_divider = {"type": "divider"}
	blocks.append(bottom_divider)
	
	try:
		client.chat_postMessage(
			channel=convo_id,
			text="Happy Friday! :tada: Here's your weekly portfolio update:",
			blocks=blocks
    )		
	except SlackApiError as e:
		print(f"Error: {e}")

def get_convo_id():		
    channel_name = "test-alerts" # temporary
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

@app.command("/stock")
def run_stock_command(ack, say, command, logger):	
	ack()	
	user_symbol = command['text']
	plain_error_text = plain_api_error(user_symbol)
	rich_error_text = rich_api_error(user_symbol)

	try:
		stock_data, stock_content = generate_stock_info(user_symbol)		
		say(
			text=f"Here's your update for {stock_data['long_name']}",
			blocks=stock_content
		)
	except KeyError:
		say(
			text=plain_error_text,
			blocks=rich_error_text
		)
	except Exception as e:
		say(
			text=generic_error_text
		)	

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)
flask_app.wsgi_app = WhiteNoise(flask_app.wsgi_app, root='static/')

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
	return handler.handle(request)
