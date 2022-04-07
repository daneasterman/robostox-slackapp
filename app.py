import os
import logging
from slack_bolt import App
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_sdk.oauth.installation_store import FileInstallationStore
from slack_sdk.oauth.state_store import FileOAuthStateStore
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from flask import Flask, request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from features.stock_command import generate_stock_info
from features.crypto_command import generate_crypto_info
from home_screen import home_screen
from python_data.app_errors import (
	plain_stock_error, 
	plain_crypto_error, 
	rich_stock_error,
	rich_crypto_error,
	generic_error_text,
	plain_no_entry
)
from database import oauth_state_store, installation_store
from config import SLACK_SIGNING_SECRET, SLACK_CLIENT_ID, SLACK_CLIENT_SECRET

# logging.basicConfig(level=logging.DEBUG)

oauth_settings = OAuthSettings(
    client_id=SLACK_CLIENT_ID,
    client_secret=SLACK_CLIENT_SECRET,
    scopes=["chat:write", "commands", "chat:write.public"],
    installation_store=installation_store,
    state_store=oauth_state_store,
)
app = App(signing_secret=SLACK_SIGNING_SECRET, oauth_settings=oauth_settings)
handler = SlackRequestHandler(app)

# Initialise Firestore
cred = credentials.Certificate({
	"type": "service_account",
	"project_id": str(os.getenv('FIREBASE_PROJECT_ID')),
	"private_key": str(os.getenv('FIREBASE_PRIVATE_KEY')).replace("\\n", "\n"),
	"token_uri": "https://oauth2.googleapis.com/token",
	"client_email": str(os.getenv('FIREBASE_CLIENT_EMAIL'))
})

firebase_admin.initialize_app(cred)
db = firestore.client()

# Start Slack App
flask_app = Flask(__name__)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
	return handler.handle(request)

@flask_app.route("/slack/install", methods=["GET"])
def install():
	return handler.handle(request)

@flask_app.route("/slack/oauth_redirect", methods=["GET"])
def oauth_redirect():
	return handler.handle(request)

@app.middleware
def log_request(logger, body, next):
	logger.debug(body)
	return next()

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
	user_name = command['user_name']
	try:
		user_symbol = command['text']	
		try:
			long_name, stock_content = generate_stock_info(user_symbol, user_name)		
			say(
				text=f"Here's your update for {long_name}",
				blocks=stock_content
			)
		except KeyError:
			say(
				text=plain_stock_error(user_symbol),
				blocks=rich_stock_error(user_symbol)
			)	
		except Exception as e:
			say(
				text=generic_error_text
			)
	except KeyError:
		say(text=plain_no_entry())

def get_db_coin_id(user_symbol):
	coins_ref = db.collection("coins")
	doc_ref = coins_ref.document(user_symbol)
	doc = doc_ref.get()
	coin_id = doc.to_dict().get("coin_id")
	return coin_id

@app.command("/coin")
def run_crypto_command(ack, say, command, logger):	
	ack()
	user_name = command['user_name']
	try: 
		user_symbol = command['text']
		try:
			coin_id = get_db_coin_id(user_symbol.lower())
			long_name, crypto_content = generate_crypto_info(coin_id, user_name)
			say(
				text=f"Here's your update for: {long_name}",
				blocks=crypto_content
			)
		except AttributeError:
			say(
				text=plain_crypto_error(user_symbol),
				blocks=rich_crypto_error(user_symbol)
			)		
		except Exception as e:
			say(text=generic_error_text)
	except KeyError:
		say(text=plain_no_entry())