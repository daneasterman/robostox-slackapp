import os
import json
import yfinance as yf
from numerize import numerize
from datetime import datetime, time, timedelta
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from flask import Flask, request, jsonify
from whitenoise import WhiteNoise

from generate_stock import generate_stock_info
from multi_external_select import multi_external_select

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
				"blocks": multi_external_select
      }
    )  
  except Exception as e:
    logger.error(f"HOME TAB ERROR: {e}")

@app.action("external_ticker_select")
def ack_ticker_select(ack, body, client, action):
	ack()	
	print(body)


@app.command("/stock")
def run_stock_command(ack, say, command, logger):
	ack()	
	user_symbol = command['text']
	try:
		stock_data, stock_content = generate_stock_info(user_symbol)
		say(
			text=f"Here's your update for {stock_data['long_name']}",
			blocks=stock_content
		)
		# To do: error text can be cleaned up:
	except KeyError:
		say(
			text=f"Sorry, the ticker symbol {user_symbol} was not found. Are you sure you spelt it correctly? You can find more stock ticker symbols on: Yahoo Finance.",
			blocks=[{
				"type": "section",
				"text": {"type": "mrkdwn", "text": f"Sorry, the ticker symbol *{user_symbol}* was not found. Are you sure you spelt it correctly? You can find more stock ticker symbols on: <https://finance.yahoo.com/|Yahoo Finance>"}
				}]
		)
	except Exception as e:
		say(
			text=f"Sorry, something has gone wrong. Please contact the creator of this app here: daniel.easterman@gmail.com for help or more information."
		)
		logger.error(f"COMMAND ERROR: {e}")

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)
# For static images:
flask_app.wsgi_app = WhiteNoise(flask_app.wsgi_app, root='static/')


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
	return handler.handle(request)

@flask_app.route('/tickers', methods=['GET', 'POST'])
def ticker_data():
	with open('data/premium/stocks/prod/nyse_nasdaq.json') as tickers_file:
		py_data = json.load(tickers_file)
		return jsonify(py_data)


# Works when running python app.py:
if __name__ == "__main__":
	flask_app.run(debug=True, port=3000)