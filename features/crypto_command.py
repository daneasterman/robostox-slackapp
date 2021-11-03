import time
from pycoingecko import CoinGeckoAPI
from numerize import numerize
from datetime import datetime
from dateutil.relativedelta import relativedelta
from utils.get_percent_change import get_percent_change

def get_period_change(coin_variable, period):
	cg = CoinGeckoAPI()
	now = datetime.now().astimezone()
	now_unix_timestamp = str(now.timestamp())
	period_delta = relativedelta(days=period)
	period_datetime = now + period_delta
	period_unix_timestamp = str(period_datetime.timestamp())
	raw_week_change = cg.get_coin_market_chart_range_by_id(
																		id=coin_variable, 
																		vs_currency="usd", 
																		from_timestamp=period_unix_timestamp, 
																		to_timestamp=now_unix_timestamp)
	period_start = raw_week_change['prices'][0][1]
	period_end = raw_week_change['prices'][-1][1]
	period_percent_change = get_percent_change(period_start, period_end)
	return period_percent_change

def generate_crypto_info():
	cg = CoinGeckoAPI()
	coin_variable = 'bitcoin'
	get_price = cg.get_price(ids=coin_variable, 
																	vs_currencies='usd', 
																	include_market_cap=True, 
																	include_24hr_vol=True,
																	include_24hr_change=True)

	raw_price = get_price[coin_variable]['usd']
	rounded_price = round(raw_price, 2)
	raw_marketcap = get_price[coin_variable]['usd_market_cap']
	marketcap = numerize.numerize(raw_marketcap, 2)
	raw_volume = get_price[coin_variable]['usd_24h_vol']
	volume = numerize.numerize(raw_volume, 2)
	day_percent_change = get_price[coin_variable]['usd_24h_change']
	
	get_coin_content = cg.get_coin_by_id(id=coin_variable, developer_data=False, sparkline=False, 
			community_data=False, localization=False, market_data=False, tickers=False)	
	logo = get_coin_content['image']['large']
	symbol = get_coin_content['symbol'].upper()	

	crypto_data = {	
		'price': format(rounded_price, ','),
		'marketcap': marketcap,
		'volume': volume,
		'day_percent_change': round(day_percent_change, 2),
		'logo': logo,
		'symbol': symbol,
		'week_percent_change': round(get_period_change(coin_variable, -6), 2),
		'month_percent_change': round(get_period_change(coin_variable, -30), 2),
		'year_percent_change': round(get_period_change(coin_variable, -365), 2)
	}

	print('**crypto_data_obj', crypto_data)	

generate_crypto_info()