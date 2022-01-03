bullet_1 = "You can use upper or lowercase for stock or crypto symbols - it doesn’t matter what you choose, whatever is more convenient for you!"

bullet_2 = "It is normal for there to be a very slight delay for the information to appear after typing your command."

bullet_3 = "Use the message tab above if you want to test things out privately before typing the commands in a shared public channel."

home_screen = [
	{
			"type": "image",
			"image_url": "https://i.imgur.com/nP5Iu5K.png",
			"alt_text": "robostox header"
		},
	{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "\n\n",				
			}
		},
	{
		"type": "section",
		"text": {
			"type": "mrkdwn",
			"text": "Hey, 👋 welcome to *RoboStox*! This app has *two* simple commands you can use to get information on stocks and crypto:"
		}
	},
	{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "\n\n",				
			}
		},
	{
		"type": "divider"
	},
	{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "\n\n",				
			}
		},
	{
		"type": "section",
		"text": {
			"type": "mrkdwn",
			"text": "*1️⃣ Use the `/stock` command.* \n\n Type `/stock` followed by the stock ticker symbol. For example: `/stock tsla` for information on *Tesla*. \n\n RoboStox supports every stock available on Yahoo Finance. All price data is provided in the local currency of the stock exchange that the company is listed on."
		}
	},
	{
		"type": "header",
			"text": {
				"type": "plain_text",
				"text": "\n\n",				
			}
		},	
	{
		"type": "section",
		"text": {
			"type": "mrkdwn",
			"text": "*2️⃣ Use the `/coin` command.* \n\n Type `/coin` followed by the crypto (coin) symbol. For example: `/coin btc` for price information on *Bitcoin*. \n\n This app supports the top 1000 crypto assets by market cap, denominated in US Dollars. Additional crypto assets can be added on request."
		}
	},
	{
		"type": "header",
			"text": {
				"type": "plain_text",
				"text": "\n\n",				
			}
		},
	{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*A few extra things to note:*"
			}
		},
	{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f" • {bullet_1} \n\n • {bullet_2} \n\n • {bullet_3}"
			}
		},
	{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "You can contact me at hellorobostox@gmail.com if you need help, have any questions, or would like to request additional crypto assets for this app."
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "\n\n"
			}
		},
	{
		"type": "divider"
	},	
]