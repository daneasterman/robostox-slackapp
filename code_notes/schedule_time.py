from datetime import datetime, time, timedelta

# Initialise as current tz time:
every_friday = datetime.now().astimezone()
while every_friday.weekday() != 4:
    every_friday += timedelta(1)

scheduled_time = time(hour=10, minute=00)
scheduled_timestamp = datetime.combine(every_friday, scheduled_time).strftime('%s')
print(scheduled_timestamp)
