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

def generate_stock_info(symbol, user_name):
	stock = yf.Ticker(symbol)	
	previous_close = stock.info['previousClose']
	current_price = stock.info['regularMarketPrice']
	raw_marketcap = stock.info['marketCap']
	marketcap = numerize.numerize(raw_marketcap, 2)
	raw_volume = stock.info['averageVolume']
	volume = numerize.numerize(raw_volume, 2)
	logo = stock.info['logo_url']
	is_valid_image = check_valid_image(logo)	
	currency_code = stock.info['currency'].upper()
	currency_symbol = get_currency_symbol(currency_code)
		
	stock_data = {
			'symbol': stock.info['symbol'],
			'long_name': stock.info['longName'],
			'logo': logo if is_valid_image else "https://i.imgur.com/2023VBv.jpg",
			'current_price': round(current_price, 2),
			'marketcap': marketcap,
			'volume': volume,
			'day_percent_change': round(get_percent_change(previous_close, current_price), 2),
			'week_percent_change': round(get_period_change(stock, "5d"), 2),
			'month_percent_change': round(get_period_change(stock, "1mo"), 2),
			'year_percent_change': round(get_period_change(stock, "ytd"), 2)
	}
	
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
			"text": f"*Price:* {currency_symbol}{stock_data['current_price']} \n\n *Market Cap:* {currency_symbol}{stock_data['marketcap']} \n *Volume:* {currency_symbol}{stock_data['volume']} \n\n *24hr:*  {stock_data['day_percent_change']}% \n *5d:*  {stock_data['week_percent_change']}% \n *30d:*  {stock_data['month_percent_change']}% \n *1yr:*  {stock_data['year_percent_change']}%"
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