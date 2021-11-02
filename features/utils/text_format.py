def natural_lang(percent):
	if percent == 0:
		return "unchanged"
	elif percent > 0:
		return "up"
	elif percent < 0:
		return "down"

def show_percent(week_change):
	if week_change == 0:
		return ""
	else:		
		return f"`{week_change}%` "