# from requests.api import options # not in use for now.
from python_data.local_tickers import local_tickers

multi_internal_select = [
  {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "Select which stocks you would like to receive notifications for:*"
      },
      "accessory": {
        "action_id": "ticker_select",
        "type": "multi_static_select",
        "placeholder": {
          "type": "plain_text",
          "text": "Select Stocks"
        },
        "options": local_tickers
    },
  }
]

multi_external_select = [{
    "type": "section",
    "text": {
      "type": "mrkdwn",
      "text": "*EXTERNAL Select your stocks to receive notifications:*"
    },
    "accessory": {
      "action_id": "external_ticker_select",
      "type": "multi_external_select",
      "placeholder": {
        "type": "plain_text",
        "text": "Select items"
      },
      "min_query_length": 2
    }
  }
]