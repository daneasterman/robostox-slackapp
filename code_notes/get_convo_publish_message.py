	client = WebClient(SLACK_BOT_TOKEN)
	def get_convo_id():		
    channel_name = "test-alerts"
    convo_id = None
    try:
        for result in client.conversations_list():
            if convo_id is not None:
                break
            for channel in result["channels"]:
                if channel["name"] == channel_name:
                    convo_id = channel["id"]                    
                    return convo_id                    

    except SlackApiError as e:
        print(f"Error: {e}")


def publish_message():
    convo_id = get_convo_id()
    stock_data = get_single_stock()
    stock_content = render_stock_content()
    try:    
        result = client.chat_postMessage(
            channel=convo_id,
            text=f"Here's your update for {stock_data['long_name']}",
            blocks=stock_content
        )
        print(result)

    except SlackApiError as e:
        print(f"Error: {e}")

# Call function:
publish_message()