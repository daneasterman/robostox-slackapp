def plain_stock_error(user_symbol):	
	return f"Sorry, the ticker symbol {user_symbol} was not found. Are you sure you spelt it correctly? You can find more stock ticker symbols o Yahoo Finance."

def plain_crypto_error(user_symbol):	
	return f"Sorry, the symbol {user_symbol} was not found. Are you sure you spelt it correctly? You can find more stock ticker symbols on CoinGecko."

def rich_stock_error(user_symbol):
	rich_error_text = [{
				"type": "section",
				"text": {"type": "mrkdwn", "text": f"Sorry, the ticker symbol *{user_symbol}* was not found. Are you sure you spelt it correctly? You can find more stock ticker symbols on: <https://finance.yahoo.com/|Yahoo Finance>"}
				}]
	return rich_error_text

def rich_crypto_error(user_symbol):
	rich_error_text = [{
				"type": "section",
				"text": {"type": "mrkdwn", "text": f"Sorry, the crypto symbol *{user_symbol}* was not found. Are you sure you spelt it correctly? You can find more symbols for crypto assets on: <https://www.coingecko.com/|CoinGecko>\n\nAlternatively, *{user_symbol}* might not be included in our top 1000 crypto assets by market cap. You can contact: robostox@gmail.com to have it added."}
				}]
	return rich_error_text

generic_error_text = "Sorry, something has gone wrong. Please contact robostox@gmail.com for help or more information."
