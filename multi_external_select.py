multi_external_select = [{
    "type": "section",
    "block_id": "core_app",
    "text": {
      "type": "mrkdwn",
      "text": "*Select your stocks to receive notifications:*"
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