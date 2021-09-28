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

from features.stock_command.generate_single import generate_stock_info, get_period_percent_change
from python_data.menus import multi_internal_select
from python_data.home_screen import home_screen
from python_data.modal import modal
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
def open_home_tab(client, event, logger):
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
def open_modal(ack, body, client, view, logger):
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

# Change this to a button handler.
@app.view("modal_view")
def handle_modal_submit(ack, body, client, view, logger):
	user = body["user"]["id"]
	state_values = view["state"]["values"]
	radio_choice = state_values["realtime_radio_input"]["toggle_realtime"]["selected_option"]["value"]
	# Pass this into old ticker select func:
	multi_select_options = state_values["multi_select_input"]["ticker_select"]["selected_options"]
	ack()	
	doc_watch = None
	if radio_choice == "REALTIME_ON":		
		entries_ref = db.collection("entries")
		latest_doc = entries_ref.limit(1)
		doc_watch = latest_doc.on_snapshot(on_snapshot)
	else:
		doc_watch.unsubscribe()
	msg = ""
	try:
		 msg = "Awesome! :white_check_mark: Your notification settings have now been saved.\n\nYou can change this at any time, you just need but re-enter these settings when you open the modal window again."
	except:
		msg = "Something went wrong, your settings were not saved. Please contact: daniel.easterman@gmail.com if the problem persists."
	try:
		client.chat_postMessage(channel=user, text=msg)
	except Exception as e:
		logger.exception(f"Failed to post a message: {e}")

callback_done = threading.Event()
def on_snapshot(doc_snapshot, changes, read_time):
	for doc in doc_snapshot:
		print(f'Received document snapshot: {doc.id}')
		# Execute another function in here with data.
	callback_done.set()


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
