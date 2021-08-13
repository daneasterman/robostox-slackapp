import csv 
import json 

json_array = []
    
with open('csv_work/cik_tickers.csv', encoding='utf-8') as csvfile:
	csv_reader = csv.DictReader(csvfile, delimiter='|')
	for row in csv_reader:
		full_obj = {
			"text": {
				"text": f"{row['Name']} - {row['Ticker']}",
				"type": "plain_text",				
			},
			"value": f"{row['Ticker']} - {row['CIK']}"
		}		
		json_array.append(full_obj)
		
	# print(json_array[20])

# output as indented json for easy copy/paste
with open('csv_work/cik_tickers_no_indent.json', 'w') as outfile:
	json.dump(json_array, outfile)
