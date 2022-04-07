import yfinance as yf
from numerize import numerize
from utils.get_currency_symbol import get_currency_symbol
from utils.check_valid_image import check_valid_image
from utils.get_percent_change import get_percent_change

def get_period_change(stock, period):
    df_period = stock.history(period=period)
    period_start = df_period.Open.iat[0]
    period_end = df_period.Close.iat[-1]
    period_percent_change = get_percent_change(period_start, period_end)
    return period_percent_change

def toggle_marketcap(rawcap, currency_symbol):
	if rawcap:
		clean_cap = numerize.numerize(rawcap, 2)
		return f"*Market Cap:* {currency_symbol}{clean_cap} \n"
	else:
		return f"*Market Cap:* N/A \n"

def generate_stock_info(symbol, user_name):
	stock = yf.Ticker(symbol)	
	previous_close = stock.info['previousClose']
	current_price = stock.info['regularMarketPrice']			
	logo = stock.info['logo_url']
	is_valid_image = check_valid_image(logo)
	currency_code = stock.info['currency'].upper()
	currency_symbol = get_currency_symbol(currency_code)
	price_hist = stock.history(period="max")
	raw_ath = price_hist['High'].max()
	rounded_ath = round(raw_ath, 2)
		
	stock_data = {
			'symbol': stock.info['symbol'],
			'long_name': stock.info['longName'],
			'logo': logo if is_valid_image else "https://i.imgur.com/2023VBv.jpg",
			'current_price': round(current_price, 2),
			'display_marketcap': toggle_marketcap(stock.info['marketCap'], currency_symbol),
			'ath_price': format(rounded_ath, ','),
			'day_percent_change': round(get_percent_change(previous_close, current_price), 2),
			'week_percent_change': round(get_period_change(stock, "5d"), 2),
			'month_percent_change': round(get_period_change(stock, "1mo"), 2),
			'year_percent_change': round(get_period_change(stock, "ytd"), 2),
	}

	price_content = f"*Price:* `{currency_symbol}{stock_data['current_price']}` \n\n"
	# mcap content here is dealt with in toggle_marketcap func above
	ath_price_content = f"*ATH Price:* {currency_symbol}{stock_data['ath_price']} \n\n"
	day_content = f"*24hr:* {stock_data['day_percent_change']}% \n"
	week_content = f"*5d:* {stock_data['week_percent_change']}% \n"
	month_content = f"*30d:*  {stock_data['month_percent_change']}% \n"
	year_content = f"*1yr:*  {stock_data['year_percent_change']}%"
	
	stock_content = [
		{
		"type": "section",
		"text": {
			"type": "mrkdwn",
			"text": f"@{user_name} just requested information on *{stock_data['long_name']}* with: `/stock`"
			}
		},
		{
		"type": "header",
		"text": {
			"type": "plain_text",
			"text": f":chart_with_upwards_trend:  {stock_data['long_name']}  |  {stock_data['symbol']}",
			"emoji": True
		}
	},
	{
		"type": "section",
		"text": {
			"type": "mrkdwn",
			"text": f"{price_content} {stock_data['display_marketcap']} {ath_price_content} {day_content} {week_content} {month_content} {year_content}"
		},
		"accessory": {
			"type": "image",
			"image_url": f"{stock_data['logo']}",
			"alt_text": "company logo"
		}
	},
	{
		"type": "section",
		"text": {
			"type": "mrkdwn",
			"text": f"*View Charts:* <https://finance.yahoo.com/quote/{stock_data['symbol']}|Yahoo Finance | {stock_data['long_name']}>",
		}
	},
	{
		"type": "divider"
	}]
	
	return stock_data['long_name'], stock_content