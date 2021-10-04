# radio_choice = state_values["realtime_radio_input"]["toggle_realtime"]["selected_option"]["value"]

# if radio_choice == "REALTIME_ON":
# 		latest_doc.on_snapshot(on_snapshot)
# 	elif radio_choice == "REALTIME_OFF":
# 		latest_doc.on_snapshot(on_snapshot).unsubscribe()

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