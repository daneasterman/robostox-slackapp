def generate_first_yes_match(filing):
	first_yes_match = [
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": f"\n\nAwesome! :white_check_mark:  You are now set-up to receive *real-time alerts.* \n\n*This is exciting!* One of the companies you just selected - *{filing['company_name']}* recently filed `Form {filing['form_type']}` on {filing['human_date']}.\n\n *Why is this important?*\n{filing['form_explanation']}\n\n*View more information on the filing here:* {filing['filing_link']}\n\n *Note:*\nWhen one of your companies files additional reports with the SEC you will receive more notifications here.\n\nYou can change the companies you follow at any time, all you need to do is re-enter the selections you just submitted."
				}
			},
			{
				"type": "divider"
			}
		]
	return first_yes_match