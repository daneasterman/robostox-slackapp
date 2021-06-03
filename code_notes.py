import json
import requests

slack_data = {'text': "Simple python proof of concept!"}

response = requests.post(
    WEBHOOK_URI, data=json.dumps(slack_data),
    headers={'Content-Type': 'application/json'}
)
if response.status_code != 200:
    raise ValueError(
        'Request to slack returned an error %s, the response is:\n%s'
        % (response.status_code, response.text)
    )