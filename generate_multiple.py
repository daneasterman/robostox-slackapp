import yfinance as yf
from generate_single import get_period_percent_change

def get_multiple_stocks(tickers):
	stocks_list = []
	for t in tickers:
		stock = yf.Ticker(t)
		stock_dict = {
			'long_name': stock.info['longName'],
			'week_percent_change': round(get_period_percent_change(stock, "5d"), 2)
		}
		stocks_list.append(stock_dict)
	return stocks_list

# def render_multiple_content()
	# calls the above function
	# Gets run in publish message
