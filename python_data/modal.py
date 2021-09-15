from python_data.local_tickers import local_tickers

modal = [
		{
			"type": "section",
			"block_id": "stocks-modal",
			"text": {
				"type": "mrkdwn",
				"text": "Hello, Assistant to the Regional Manager Dwight! Here are a few Robostox settings.\n\n"
			}
		},
		{
			"label": {
				"type": "plain_text",
				"text": "Please choose your notification options:"
			},
			"type": "input",
			"element": {
				"action_id": "toggle_realtime",
				"type": "radio_buttons",
				"initial_option": {
					"value": "REALTIME_OFF",
					"text": {
						"type": "plain_text",
						"text": "Off"
					}
				},
				"options": [
					{
						"value": "REALTIME_OFF",
						"text": {
							"type": "plain_text",
							"text": "Off"
						}
					},
					{
						"value": "REALTIME_ON",
						"text": {
							"type": "plain_text",
							"text": "On"
						}
					}					
				]
			},
		},
		{
			"label": {
				"type": "plain_text",
				"text": "Please choose your notification options:\n\n"
			},
			"type": "input",
			"element": {
				"action_id": "ticker_select",
				"type": "multi_static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Apple, Tesla, Amazon etc."
				},
				"options": local_tickers
				}
			}
	]	