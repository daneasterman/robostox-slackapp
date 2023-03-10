from slack_sdk import WebClient

SLACK_BOT_TOKEN = str(os.getenv('SLACK_BOT_TOKEN'))
client = WebClient(SLACK_BOT_TOKEN)

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