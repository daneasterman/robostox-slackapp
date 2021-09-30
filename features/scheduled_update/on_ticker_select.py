def natural_lang(percent):
	if percent == 0:
		return "unchanged"
	elif percent > 0:
		return "up"
	elif percent < 0:
		return "down"

def show_percent(week_change):
	if week_change == 0:
		return ""
	else:		
		return f"`{week_change}%` "

@app.action("ticker_select")
def ticker_select(ack, action):
	ack()
	tickers = []
	cik_codes = []
	stocks_list =[]
	selected_options = action['selected_options']	
	for s in selected_options:
		split_value = s['value'].split()	
		tickers.append(split_value[0])
		cik_codes.append(split_value[2])
	
	for t in tickers:
		stock = yf.Ticker(t)
		week_change = round(get_period_percent_change(stock, "5d"), 2)
		current_price = stock.info['regularMarketPrice']
		stock_dict = {
			'long_name': stock.info['longName'],
			'current_price': round(current_price, 2),
			'week_change': 0 if week_change == 0 else week_change
			}
		stocks_list.append(stock_dict)
	# publish_scheduled_message(stocks_list)

	# This will change to scheduler in prod:
client = WebClient(SLACK_BOT_TOKEN)
def publish_scheduled_message(stocks_list, logger):
	convo_id = get_convo_id()

	blocks = []
	intro = {
		"type": "section",
		"text": {
			"type": "mrkdwn",
			"text": "*Happy Friday!*  :tada:  Here's your weekly portfolio update :chart_with_upwards_trend:"
		}
	}
	blocks.append(intro)
	top_divider = {"type": "divider"}
	blocks.append(top_divider)

	for s in stocks_list:
		week_change = s['week_change']
		main_info = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"*{s['long_name']}* is trading at `${s['current_price']}` and is *{natural_lang(week_change)}* {show_percent(week_change)}for the week."
			},
		}
		blocks.append(main_info)
	
	bottom_divider = {"type": "divider"}
	blocks.append(bottom_divider)
	
	try:
		client.chat_postMessage(
			channel=convo_id,
			text="Happy Friday! :tada: Here's your weekly portfolio update:",
			blocks=blocks
    )		
	except SlackApiError as e:
		logger(f"PUBLISH_SCHEDULED_MSG ERROR: {e}")