from python_data.local_tickers import local_tickers

modal = [
		{
			"type": "section",
			"block_id": "stocks_modal",
			"text": {
				"type": "mrkdwn",
				"text": "Hello, Assistant to the Regional Manager Dwight! Here are a few Robostox settings.\n\n"
			}
		},
		{
			"label": {
				"type": "plain_text",
				"text": "Switch your real-time notifications off or on:"
			},
			"type": "input",
			"block_id": "radio_input",
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
				"text": "Select your stocks to receive real-time filing notifications:\n\n"
			},
			"type": "input",
			"block_id": "multi_select_input",
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