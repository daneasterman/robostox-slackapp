static_menu_content = [{
		"type": "section",
		"text": {
			"type": "mrkdwn",
			"text": "*Select which stocks you would like to receive notifications for:*"
		},
		"accessory": {
			"action_id": "ticker_select",
			"type": "multi_static_select",
			"placeholder": {
				"type": "plain_text",
				"text": "Select Stocks"
			},
			"options": [
			{
				"text": {
					"type": "plain_text",
					"text": "Tesla, Inc."
				},
				"value": "TSLA"
			},
			{
				"text": {
					"type": "plain_text",
					"text": "Microsoft Corporation"
				},
				"value": "MSFT"
			},
			{
				"text": {
					"type": "plain_text",
					"text": "Apple Inc."
				},
				"value": "AAPL"
			}
		]
	}
}]