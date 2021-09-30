# company_name = filing['company_name']
# form_type = filing['form_type']
# form_explanation = filing['form_explanation']
# human_date =  filing['human_date']

def generate_first_message():
	confirm_content = [
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "\n\n*Awesome!* :white_check_mark:  You are now set-up to receive real-time alerts. \n\nWhen one of the companies you selected files a report with the SEC you will receive a notification here.\n\nYou can change the companies you follow at any time, you just need to re-enter these selections when you click the Set-Up button on the home screen again."
				}
			},
			{
				"type": "divider"
			}
		]
	return confirm_content


def generate_main_filing_message(filing):
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
	