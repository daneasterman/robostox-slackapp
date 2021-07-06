# Read clean-nyse-sample
# iterate over the json and print out values

import json
import pprint

new_json = {}
new_json['options'] = []

with open('nyse_sample.json') as in_file:
	source_data = json.load(in_file)
	for s in source_data:
		new_json['options'].append({
		"text": {
			"type": "plain_text",
			"text": s['Name']
		}
})

with open('new_file.json', 'w') as outfile:
	json.dump(new_json, outfile, indent=4)