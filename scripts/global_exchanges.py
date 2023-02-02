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

# London stock exchange
with open('data/premium/stocks/raw/lse.json') as lse_file:
	lse_data = json.load(lse_file)
	for s in lse_data:
		new_json['options'].append({
		"text": {
			"type": "plain_text",
			"text": f"{s['Name']} - {s['Code']}",			
		},
		"value": s["Code"]
})

with open('data/premium/stocks/raw/toronto.json') as toronto_file:
	toronto_data = json.load(toronto_file)
	for s in toronto_data:
		new_json['options'].append({
		"text": {
			"type": "plain_text",
			"text": f"{s['Name']} - {s['Code']}",			
		},
		"value": s["Code"]
})

with open('data/premium/stocks/raw/australia.json') as australia_file:
	aus_data = json.load(australia_file)
	for s in aus_data:
		new_json['options'].append({
		"text": {
			"type": "plain_text",
			"text": f"{s['Name']} - {s['Code']}",			
		},
		"value": s["Code"]
})

# Singapore:
with open('data/premium/stocks/raw/sg.json') as sg_file:
	sg_data = json.load(sg_file)
	for s in sg_data:
		new_json['options'].append({
		"text": {
			"type": "plain_text",
			"text": f"{s['Name']} - {s['Code']}",
		},
		"value": s["Code"]
})

# Hong Kong:
with open('data/premium/stocks/raw/hk.json') as hk_file:
	hk_data = json.load(hk_file)
	for s in hk_data:
		new_json['options'].append({
		"text": {
			"type": "plain_text",
			"text": f"{s['Name']} - {s['Code']}",			
		},
		"value": s["Code"]
})

# National Stock Exchange - India:
with open('data/premium/stocks/raw/nse.json') as nse_file:
	nse_data = json.load(nse_file)
	for s in nse_data:
		new_json['options'].append({
		"text": {
			"type": "plain_text",
			"text": f"{s['Name']} - {s['Code']}",			
		},
		"value": s["Code"]
})

with open('all_exchanges.json', 'w') as outfile:
	json.dump(new_json, outfile)

print('nyse_data', len(nyse_data))
print('nasdaq_data', len(nasdaq_data))
print('lse_data', len(lse_data))
print('toronto_data', len(toronto_data))
print('aus_data', len(aus_data))
print('sg_data', len(sg_data))
print('hk_data', len(hk_data))
print('nse_data', len(nse_data))

print('TOTAL:', len(new_json['options']))