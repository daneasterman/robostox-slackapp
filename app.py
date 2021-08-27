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

from python_data.menus import multi_internal_select
from python_data.home_screen import home_screen
from python_data.modal import modal

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
def display_home_tab(client, event, logger):
  try:    
    client.views_publish(      
      user_id=event["user"],
      view={
        "type": "home",
        "callback_id": "home_view",
				"blocks": home_screen
      }
    )  
  except Exception as e:
    logger.error(f"HOME TAB ERROR: {e}")

@app.action("launch_modal_btn")
def launch_modal(ack, body, client, logger):
	ack()
	try: 
		client.views_open(
			trigger_id=body["trigger_id"],
			view={
				"type": "modal",
				"callback_id": "modal_view",
				"title": {"text": "Your Robostox Setup", "type": "plain_text"},
				"submit": {"text": "Submit", "type": "plain_text"},
				"blocks": modal
			}
		)
	except Exception as e:
		logger.error(f"MODAL ERROR: {e}")	


@app.action("ticker_select")
def ticker_select(ack, action):
	ack()
	tickers = []
	cik_codes = []
	stocks_list =[]
	selected_options = action['selected_options']	
	for s in selected_options:
		split_value = s['value'].split()
		tickers.append(split_value[0])
		cik_codes.append(split_value[2])
	
	for t in tickers:
		stock = yf.Ticker(t)
		week_change = round(get_period_percent_change(stock, "5d"), 2)
		current_price = stock.info['regularMarketPrice']
		stock_dict = {
			'long_name': stock.info['longName'],
			'current_price': round(current_price, 2),
			'week_change': 0 if week_change == 0 else week_change
			}
		stocks_list.append(stock_dict)		
	publish_message(stocks_list)

def natural_lang(percent):
	if percent == 0:
		return "unchanged"
	elif percent > 0:
		return "up"
	elif percent < 0:
		return "down"

def show_percent(week_change):
	if week_change == 0:
		return ""
	else:		
		return f"`{week_change}%` "

# This will change to scheduler in prod:
client = WebClient(SLACK_BOT_TOKEN)
def publish_message(stocks_list):
	convo_id = get_convo_id()

	blocks = []
	intro = {
		"type": "section",
		"text": {
			"type": "mrkdwn",
			"text": "*Happy Friday!*  :tada:  Here's your weekly portfolio update :chart_with_upwards_trend:"
		}
	}
	blocks.append(intro)
	top_divider = {"type": "divider"}
	blocks.append(top_divider)

	for s in stocks_list:
		week_change = s['week_change']		
		main_info = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"*{s['long_name']}* is trading at `${s['current_price']}` and is *{natural_lang(week_change)}* {show_percent(week_change)}for the week."
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
		print(f"PUBLISH MSG ERROR: {e}")

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
