# Read clean-nyse-sample
# iterate over the json and print out values

import json
import pprint

new_json = {}
new_json['options'] = []

with open('data/premium/stocks/raw/nyse.json') as nyse_file:
	nyse_data = json.load(nyse_file)
	for s in nyse_data:
		new_json['options'].append({
		"text": {
			"type": "plain_text",
			"text": f"{s['Name']} - {s['Code']}",
			"exchange": s["Exchange"]
		},
		"value": s["Code"]
})

with open('data/premium/stocks/raw/nasdaq.json') as nasdaq_file:
	nasdaq_data = json.load(nasdaq_file)
	for s in nasdaq_data:
		new_json['options'].append({
		"text": {
			"type": "plain_text",
			"text": f"{s['Name']} - {s['Code']}",
			"exchange": s["Exchange"]
		},
		"value": s["Code"]
})

# with open('nyse_nasdaq_out.json', 'w') as outfile:
# 	json.dump(new_json, outfile, indent=4)
	# json.dump(new_json, outfile)


print('NYSE DATA COUNT', len(nyse_data))
print('NASDAQ DATA COUNT', len(nasdaq_data))
print(len(new_json['options']))
	