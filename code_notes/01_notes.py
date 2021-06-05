import json
import requests
from slack_sdk.webhook import WebhookClient

# Disable for now:
# from slack_bolt.adapter.flask import SlackRequestHandler
# from flask import Flask, request, Response

# try:
#     api.verify_credentials()
#     print("Authentication OK")
# except:
#     print("Error during authentication")

slack_data = {'text': "Tweet sent!"}

response = requests.post(
            WEBHOOK_URI, data=json.dumps(slack_data), 
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code != 200:
            raise ValueError(
                'Request to slack returned an error %s, the response is:\n%s'
                % (response.status_code, response.text)
            )

url = "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"
webhook = WebhookClient(url)

response = webhook.send(text="Hello!")
assert response.status_code == 200
assert response.body == "ok"