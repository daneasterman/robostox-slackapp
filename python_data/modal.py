from python_data.local_tickers import local_tickers

modal = [
		{
			"type": "section",
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
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "Select stocks to receive notifications *(Max 10)*:\n\n"
      },
      "accessory": {
        "action_id": "ticker_select",
        "type": "multi_static_select",
        "placeholder": {
          "type": "plain_text",
          "text": "Apple, Tesla etc"
        },
        "options": local_tickers
    },
  }
]