from datetime import datetime, time, timedelta

def schedule_message():
    convo_id = get_convo_id()
    every_friday = datetime.now().astimezone()
    while every_friday.weekday() != 4:
        every_friday += timedelta(1)

    scheduled_time = time(hour=11, minute=30)
    scheduled_timestamp = datetime.combine(every_friday, scheduled_time).strftime('%s')
    
    try:
        result = client.chat_scheduleMessage(
            channel=convo_id,
            text="Publish future Friday message test!",
            post_at=scheduled_timestamp
        )
        print(result)
    except SlackApiError as e:
        print(f"Error: {e}")

schedule_message()