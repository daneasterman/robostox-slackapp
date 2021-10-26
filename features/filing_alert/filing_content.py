def generate_generic_confirm():
	generic_confirm = [
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "\n\nAwesome! :white_check_mark:  You are now set-up to receive real-time alerts. \n\nWhen one of your companies files a report with the SEC you will receive a notification here.\n\nYou can change the companies you follow at any time, all you need to do is re-enter the selections you just submitted."
				}
			},
			{
				"type": "divider"
			}
		]
	return generic_confirm

def generate_filing_alert(filing):
	filing_content = [
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": f"\n\n:rotating_light: *New SEC Filing Alert* :rotating_light: \n\n *{filing['company_name']}* just filed `Form {filing['form_type']}` on {filing['human_date']}.\n\n *Why is this important?*\n{filing['form_explanation']}\n\n*View more information on the filing here:* {filing['filing_link']}"
				}
			},
			{
				"type": "divider"
			}
		]
	return filing_content
	