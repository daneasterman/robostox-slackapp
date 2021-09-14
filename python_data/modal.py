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
				"type": "checkboxes",				
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "Toggle realtime on / off"
						},
						"value": "realtime_on"
					},
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