import threading

callback_done = threading.Event()	
def on_snapshot(doc_snapshot, changes, read_time):	
	for change in changes:
		if change.type.name == 'ADDED':
			print(f'Filing: {change.document.id}')
			# filing = change.document.to_dict()			
			# publish_matched_filing(filing)
			callback_done.set()

@app.action("launch_modal_btn")
def open_modal(context, ack, body, client, view, logger):	
	ack()
	try: 
		client.views_open(
			trigger_id=body["trigger_id"],
			view={
				"type": "modal",
				# Callback id used to trigger view submission action:
				"callback_id": "modal_view",
				"title": {"text": "Your Setup", "type": "plain_text"},
				"submit": {"text": "Submit", "type": "plain_text"},
				"blocks": modal
			}
		)	
	except Exception as e:
		logger.error(f"MODAL ERROR: {e}")

@app.view("modal_view")
def handle_modal_submit(context, ack, body, client, view, logger):	
	user_id = body["user"]["id"]	
	state_values = view["state"]["values"]
	multi_select_options = state_values["multi_select_input"]["ticker_select"]["selected_options"]
	ack()
	usr_ciks = [s["value"].split()[2] for s in multi_select_options]		

	query = db.collection("entries").where('cik_code', 'in', usr_ciks)
	query_watch = query.on_snapshot(on_snapshot)

def publish_first_confirmation():
	try:
		client.chat_postMessage(
			channel=get_convo_id("test-alerts"),
			text="Awesome! :white_check_mark: You are now set-up to receive real-time alerts.",
			blocks=generate_generic_confirm()
		)
	except SlackApiError as e:
		print(f"**publish_first_confirmation error: {e}")

def publish_matched_filing(filing):	
	try:		
		client.chat_postMessage(						
			channel=get_convo_id("test-alerts"),
			text=f":rotating_light: *New SEC Filing Alert for {filing['company_name']}* :rotating_light",
			blocks=generate_filing_alert(filing)
		)
	except SlackApiError as e:
		print(f"**publish_matched_filing error: {e}")	