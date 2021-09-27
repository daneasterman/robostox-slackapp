import os
import json
import threading
import yfinance as yf
from datetime import datetime, time, timedelta
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from flask import Flask, request, jsonify
from whitenoise import WhiteNoise
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from generate_single import generate_stock_info, get_period_percent_change
from python_data.menus import multi_internal_select
from python_data.home_screen import home_screen
from python_data.modal import modal
from python_data.local_tickers import local_tickers
from python_data.app_errors import plain_api_error, rich_api_error, generic_error_text

from dotenv import load_dotenv
load_dotenv()

# Heroku automatically pulls the variables from this:
SLACK_BOT_TOKEN = str(os.getenv('SLACK_BOT_TOKEN'))
SLACK_SIGNING_SECRET = str(os.getenv('SLACK_SIGNING_SECRET'))

cred = credentials.Certificate('firestore-sdk.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

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
def launch_modal(ack, body, client, view, logger):
	ack()	
	try: 
		client.views_open(
			trigger_id=body["trigger_id"],
			view={
				"type": "modal",
				# Callback id used to trigger view submission action:
				"callback_id": "modal_view",
				"title": {"text": "Your Robostox Setup", "type": "plain_text"},
				"submit": {"text": "Submit", "type": "plain_text"},
				"blocks": modal
			}
		)
	except Exception as e:
		logger.error(f"MODAL ERROR: {e}")

callback_done = threading.Event()
def on_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        print(f'Received document snapshot: {doc.id}')
    callback_done.set()

# Change this to a button handler.
@app.view("modal_view")
def handle_modal_submit(ack, body, client, view, logger):
	user = body["user"]["id"]
	state_values = view["state"]["values"]
	radio_choice = state_values["realtime_radio_input"]["toggle_realtime"]["selected_option"]["value"]
	# Pass this into old ticker select func:
	multi_select_options = state_values["multi_select_input"]["ticker_select"]["selected_options"]
	ack()	
	# doc_watch = None
	# if radio_choice == "REALTIME_ON":
	# 	print("**REALTIME SWITCHED ON!**")
		# entries_ref = db.collection("entries")
		# latest_doc = entries_ref.limit(1)
		# doc_watch = latest_doc.on_snapshot(on_snapshot)
	# else:
	# 	doc_watch.unsubscribe()
	msg = ""
	try:
		 msg = "Awesome! :white_check_mark: Your notification settings have now been saved.\n\nYou can change this at any time, you just need but re-enter these settings when you open the modal window again."
	except:
		msg = "Something went wrong, your settings were not saved. Please contact: daniel.easterman@gmail.com if the problem persists."
	try:
		client.chat_postMessage(channel=user, text=msg)
	except Exception as e:
		logger.exception(f"Failed to post a message: {e}")


# THIS WILL NEED SOME REFACTOR:
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
	# publish_scheduled_message(stocks_list)

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
def publish_scheduled_message(stocks_list, logger):
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
		logger(f"PUBLISH_SCHEDULED_MSG ERROR: {e}")

def get_convo_id(logger):		
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
        logger(f"GET_CONVO_ID Error: {e}")

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
