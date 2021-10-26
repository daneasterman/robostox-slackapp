import yfinance as yf
from numerize import numerize
from utils.check_valid_image import check_valid_image

def percent_change(start_point, end_point):
    return((float(end_point)-start_point)/abs(start_point))*100.00

def get_period_percent_change(stock, period):
    df_period = stock.history(period=period)
    period_start = df_period.Open.iat[0]
    period_end = df_period.Close.iat[-1]
    period_percent_change = percent_change(period_start, period_end)
    return period_percent_change

def generate_stock_info(symbol):
	stock = yf.Ticker(symbol)
	
	previous_close = stock.info['previousClose']
	current_price = stock.info['regularMarketPrice']	

	raw_marketcap = stock.info['marketCap']
	marketcap = numerize.numerize(raw_marketcap, 2)
	raw_volume = stock.info['averageVolume']
	volume = numerize.numerize(raw_volume, 2)
	logo = stock.info['logo_url']
	is_valid_image = check_valid_image(logo)
		
	stock_data = {
			'symbol': stock.info['symbol'],
			'long_name': stock.info['longName'],
			'logo': logo if is_valid_image else "https://i.imgur.com/2023VBv.jpg",
			'current_price': round(current_price, 2),
			'marketcap': marketcap,
			'volume': volume,
			'target_price': stock.info['targetMeanPrice'],
			'day_percent_change': round(percent_change(previous_close, current_price), 2),
			'week_percent_change': round(get_period_percent_change(stock, "5d"), 2),
			'month_percent_change': round(get_period_percent_change(stock, "1mo"), 2),
			'year_percent_change': round(get_period_percent_change(stock, "ytd"), 2)
	}
	
	stock_content = [{
		"type": "header",
		"text": {
			"type": "plain_text",
			"text": f"{stock_data['long_name']}  |  {stock_data['symbol']}",
			"emoji": True
		}
	},
	{
		"type": "section",
		"text": {
			"type": "mrkdwn",
			"text": f"*Price:* ${stock_data['current_price']} \n\n *Market Cap:* ${stock_data['marketcap']} \n *Volume:* ${stock_data['volume']} \n\n *24hr:*  {stock_data['day_percent_change']}% \n *5d:*  {stock_data['week_percent_change']}% \n *30d:*  {stock_data['month_percent_change']}% \n *1yr:*  {stock_data['year_percent_change']}% *1yr Target Price:*  ${stock_data['target_price']}\n\n "
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
	
	return stock_data, stock_content
