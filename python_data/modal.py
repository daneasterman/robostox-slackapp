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
			"block_id": "realtime_radio_input",
			"element": {
				"action_id": "toggle_realtime",
				"type": "radio_buttons",
				"initial_option": {
					"value": "REALTIME_ON",
					"text": {
						"type": "plain_text",
						"text": "On"
					}
				},
				"options": [
					{
						"value": "REALTIME_ON",
						"text": {
							"type": "plain_text",
							"text": "On"
						}
					},
					{
						"value": "REALTIME_OFF",
						"text": {
							"type": "plain_text",
							"text": "Off"
						}
					},								
				]
			},
		},
		{
			"label": {
				"type": "plain_text",
				"text": "Receive updates for all new filings:"
			},
			"type": "input",
			"block_id": "all_updates_radio_input",
			"element": {
				"action_id": "toggle_realtime",
				"type": "radio_buttons",
				"initial_option": {
					"value": "ALL_UPDATES_YES",
					"text": {
						"type": "plain_text",
						"text": "Yes"
					}
				},
				"options": [
					{
						"value": "ALL_UPDATES_YES",
						"text": {
							"type": "plain_text",
							"text": "Yes"
						}
					},
					{
						"value": "ALL_UPDATES_NO",
						"text": {
							"type": "plain_text",
							"text": "No"
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
				"initial_options": [{ "text": { "text": "Microsoft Corp - MSFT", "type": "plain_text" }, "value": "MSFT - 000789019" }],
				"options": local_tickers
				}
			}
	]