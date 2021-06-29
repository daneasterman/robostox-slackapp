import os
import yfinance as yf
from numerize import numerize
from datetime import datetime, time, timedelta
from slack_bolt import App
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from generate_stock import generate_stock_info
from dotenv import load_dotenv
load_dotenv()

SLACK_BOT_TOKEN = str(os.getenv('SLACK_BOT_TOKEN'))
SLACK_SIGNING_SECRET = str(os.getenv('SLACK_SIGNING_SECRET'))

# Start Slack App
app = App(
		token=SLACK_BOT_TOKEN,
		signing_secret=SLACK_SIGNING_SECRET
)

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
			logger.error(f"ERROR***: {e}")


# Start Bolt app
if __name__ == "__main__":
		app.start(port=int(os.environ.get("PORT", 3000)))