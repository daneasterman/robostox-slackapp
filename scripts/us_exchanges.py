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
			# For inspection:
			# "exchange": s["Exchange"]
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
		},
		"value": s["Code"]
})

with open('nyse_nasdaq_ver2.json', 'w') as outfile:
	json.dump(new_json, outfile)
	# For inspection:
	# json.dump(new_json, outfile, indent=4)


print('NYSE DATA COUNT:', len(nyse_data))
print('NASDAQ DATA COUNT:', len(nasdaq_data))
print('TOTAL:', len(new_json['options']))