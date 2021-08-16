import requests
import re
from time import sleep
from bs4 import BeautifulSoup
import json
import urllib.parse as urlparse
from urllib.parse import parse_qs

# Test single paypal company:
# SEC_XML_URL="https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&output=atom&CIK=PYPL"

def get_xml():
	BASE_SEC_XML = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&output=atom&CIK="
	
	# hyper_curated = ['PYPL', 'TCEHY', 'BABA', 'SNAP', 'SQ', 'ZM', 'JD', 'ABNB', 'SNOW', 'UBER', 'LYFT', 'TWLO', 'DASH', 'DOCU', 'RBLX', 'PLTR', 'HOOD', 'PTON', 'WIX', 'XPEV', 'SPCE']

	spacs = ['NKLA', 'OPEN', 'CLOV', 'IPOD', 'IPOF', 'SOFI', 'PSTH', 'DKNG', 'SOFI', 'DNAA', 'DNAB', 'DNAC', 'DNAD']

	sec_urls = [BASE_SEC_XML + symb for symb in spacs]	
	
	json_array = []
	
	headers = {'User-agent': 'Mozilla/5.0'}
	for url in sec_urls:
		sleep(1)
		resp = requests.get(url, headers=headers)
		soup = BeautifulSoup(resp.content, "xml")
		print("Request made:", resp.status_code)

		CIK = soup.cik.text
		company_name = soup.find(re.compile('^conformed')).text			
		parsed = urlparse.urlparse(url)
		symbol = parse_qs(parsed.query)['CIK'][0]

		full_obj = {
			"text": {
				"text": f"{company_name} - {symbol}",
				"type": "plain_text",				
			},
			"value": f"{symbol} - {CIK}"
		}
		json_array.append(full_obj)
	
	with open('python_data/spac_tickers.json', 'w') as outfile:
		json.dump(json_array, outfile)

get_xml()

