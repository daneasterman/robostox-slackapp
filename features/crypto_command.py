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

def generate_crypto_info(coin_variable, user_name):
	cg = CoinGeckoAPI()	
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
	
	get_by_id = cg.get_coin_by_id(id=coin_variable, developer_data=False, sparkline=False, 
			community_data=False, localization=False, market_data=False, tickers=False)	
	long_name = get_by_id['name']
	logo = get_by_id['image']['large']
	symbol = get_by_id['symbol'].upper()

	crypto_data = {
		'long_name': long_name,
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

	crypto_content = [
		{
		"type": "section",
		"text": {
			"type": "mrkdwn",
			"text": f"@{user_name} just requested information on *{crypto_data['long_name']}* with: `/coin`"
			}
		},
		{
		"type": "header",
		"text": {
			"type": "plain_text",
			"text": f":chart_with_upwards_trend:  {crypto_data['long_name']}  |  {crypto_data['symbol']}",
			"emoji": True			
		}
	},
	{
		"type": "section",
		"text": {
			"type": "mrkdwn",
			"text": f"*Price:* ${crypto_data['price']} \n\n *Market Cap:* ${crypto_data['marketcap']} \n *Volume:* ${crypto_data['volume']} \n\n *24hr:*  {crypto_data['day_percent_change']}% \n *5d:*  {crypto_data['week_percent_change']}% \n *30d:*  {crypto_data['month_percent_change']}% \n *1yr:*  {crypto_data['year_percent_change']}%"
		},
		"accessory": {
			"type": "image",
			"image_url": f"{crypto_data['logo']}",
			"alt_text": "company logo"
		}
	},
	{
		"type": "section",
		"text": {
			"type": "mrkdwn",
			"text": f"*View Charts:* <https://www.coingecko.com/en/coins/{coin_variable}| CoinGecko | {crypto_data['long_name']}>",
		}
	},
	{
		"type": "divider"
	}]
	
	return long_name, crypto_content