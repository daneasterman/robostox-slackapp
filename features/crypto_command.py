import sys
from pycoingecko import CoinGeckoAPI
from numerize import numerize

# sys.path.insert(0, '/home/amninder/Desktop/Folder_2')
# sys.path.insert(0, '/stoxbot/stoxbot_v1/utils')
from utils.check_valid_image import check_valid_image

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
		'symbol': symbol
	}
	print('**crypto_data obj', crypto_data)
	

generate_crypto_info()