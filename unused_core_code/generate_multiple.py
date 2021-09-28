import yfinance as yf
# from app import ack_ticker_select
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
	print(stocks_list)

	for s in stocks_list:
		text = f"This is your stock: {s['long_name']}"
	return text



	

	# This gets run in publish message
