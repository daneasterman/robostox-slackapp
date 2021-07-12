def plain_api_error(user_symbol):	
	return f"Sorry, the ticker symbol {user_symbol} was not found. Are you sure you spelt it correctly? You can find more stock ticker symbols on: Yahoo Finance."

def rich_api_error(user_symbol):
	rich_error_text = [{
				"type": "section",
				"text": {"type": "mrkdwn", "text": f"Sorry, the ticker symbol *{user_symbol}* was not found. Are you sure you spelt it correctly? You can find more stock ticker symbols on: <https://finance.yahoo.com/|Yahoo Finance>"}
				}]
	return rich_error_text

generic_error_text = "Sorry, something has gone wrong. Please contact the creator of this app here: daniel.easterman@gmail.com for help or more information."
