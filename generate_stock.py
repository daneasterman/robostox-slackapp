import yfinance as yf
from numerize import numerize

def percent_change(start_point, end_point):
    return((float(end_point)-start_point)/abs(start_point))*100.00

def get_period_percent_change(stock, period):
    df_period = stock.history(period=period)
    period_start = df_period.Open.iat[0]
    period_end = df_period.Open.iat[-1]
    period_percent_change = percent_change(period_start, period_end)
    return period_percent_change

def get_single_stock():
    # Try block? Hardcode as MSFT for now, need to catch error here, what if API fails?
    stock = yf.Ticker("MSFT")

    previous_close = stock.info['previousClose']
    current_price = stock.info['regularMarketPrice']
    raw_marketcap = stock.info['marketCap']
    marketcap = numerize.numerize(raw_marketcap, 2)
    raw_volume = stock.info['averageVolume']
    volume = numerize.numerize(raw_volume, 2)

    stock_data = {
        'symbol': stock.info['symbol'],
        'long_name': stock.info['longName'],
        'logo': stock.info['logo_url'],
        'current_price': current_price,
        'marketcap': marketcap,
        'volume': volume,        
        'day_percent_change': round(percent_change(previous_close, current_price), 2),
        'week_percent_change': round(get_period_percent_change(stock, "5d"), 2),
        'month_percent_change': round(get_period_percent_change(stock, "1mo"), 2),
        'year_percent_change': round(get_period_percent_change(stock, "ytd"), 2)
    }
    return stock_data

def render_stock_content():
    stock_data = get_single_stock()
    content =  [{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"Hey :wave:  here's the latest price information for {stock_data['long_name']}:"
			}
		},
		{
			"type": "divider"
		},
		{
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
				"text": "*Price:*  $200 \n\n\n *Mkt Cap:*  $200,000 \n *Volume:*  $150,150 \n\n\n *24hr:* 2.0% \n *5d:* 15% \n *30d:* 25% \n *1yr:* 200%"
			},
			"accessory": {
				"type": "image",
				"image_url": "https://logo.clearbit.com/apple.com",
				"alt_text": "company logo"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*View Charts:* <https://finance.yahoo.com/quote/AAPL|Yahoo Finance | Apple>"
			}
		},
		{
			"type": "divider"
		}]
    return content
