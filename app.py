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
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from features.common.get_convo_id import get_convo_id
from features.stock_command.generate_single_stock import generate_stock_info
# from features.filing_alert.filing_content import generate_generic_confirm, generate_filing_alert

from python_data.menus import multi_internal_select
from home_screen import home_screen
from python_data.modal import modal
from python_data.app_errors import plain_api_error, rich_api_error, generic_error_text

from dotenv import load_dotenv
load_dotenv()

# Heroku automatically pulls the variables from this:
SLACK_USER_TOKEN = str(os.getenv('SLACK_USER_TOKEN'))
SLACK_BOT_TOKEN = str(os.getenv('SLACK_BOT_TOKEN'))
SLACK_SIGNING_SECRET = str(os.getenv('SLACK_SIGNING_SECRET'))
client = WebClient(SLACK_BOT_TOKEN)

# Initialise Firestore
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


@app.command("/stock")
def run_stock_command(ack, say, command, logger):	
	ack()	
	user_symbol = command['text']
	user_name = command['user_name']	
	try:
		stock_data, stock_content = generate_stock_info(user_symbol, user_name)		
		say(
			text=f"Here's your update for {stock_data['long_name']}",
			blocks=stock_content
		)
	except KeyError:
		say(
			text=plain_api_error(user_symbol),
			blocks=rich_api_error(user_symbol)
		)
	# ENSURE IN PROD:
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
