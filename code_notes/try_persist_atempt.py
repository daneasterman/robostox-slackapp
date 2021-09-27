try:
		client.views_update(
					# Pass the view_id
					view_id=body["view"]["id"],
					# String that represents view state to protect against race conditions
					hash=body["view"]["hash"],
					# View payload with updated blocks
					view={
							"type": "modal",            
							"callback_id": "modal_view",
							"title": {"text": "Updated modal", "type": "plain_text"},
							"blocks": [
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
													"value": radio_state,
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
									]
					}
			)
	except Exception as e:
		logger.error(f"HANDLE SUBMIT ERROR: {e}")
