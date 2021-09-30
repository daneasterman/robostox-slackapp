msg = ""
	try:
		 msg = "Awesome! :white_check_mark: Your notification settings have now been saved.\n\nYou can change this at any time, you just need but re-enter these settings when you open the modal window again."
	except:
		msg = "Something went wrong, your settings were not saved. Please contact: daniel.easterman@gmail.com if the problem persists."
	try:
		client.chat_postMessage(channel=user, text=msg)
	except Exception as e:
		logger.exception(f"Failed to post a message: {e}")