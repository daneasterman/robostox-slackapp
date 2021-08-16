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
	# spacs = ['NKLA', 'OPEN', 'CLOV', 'IPOD', 'IPOF', 'SOFI', 'PSTH', 'DKNG', 'SOFI', 'DNAA', 'DNAB', 'DNAC', 'DNAD']
	
	all_hyper = ['twou', 'mmm', 'amd', 't', 'abbv', 'atvi', 'adbe', 'afrm', 'api', 'abnb', 'alb', 'baba', 'googl', 'ayx', 'amzn', 'aal', 'axp', 'aapl', 'aqb', 'fuv', 'anet', 'asan', 'team', 'acb', 'adsk', 'axon', 'bidu', 'bac', 'brk-b', 'bynd', 'bigc', 'bili', 'bngo', 'ba', 'bkng', 'box', 'avgo', 'bmbl', 'ai', 'crsp', 'csiq', 'cgc', 'ccl', 'cvna', 'cspr', 'chgg', 'cvx', 'chwy', 'cmg', 'csco', 'net', 'clov', 'ko', 'coin', 'crsr', 'cost', 'coup', 'crwd', 'ddog', 'dal', 'apps', 'dis', 'docu', 'dash', 'dkng', 'dbx', 'edit', 'estc', 'ea', 'enph', 'etsy', 'xom', 'fb', 'ftch', 'fsly', 'fdx', 'fslr', 'fvrr', 'f', 'ge', 'gm', 'gpro', 'huya', 'hlt', 'ibm', 'ipgp', 'ilmn', 'intc', 'ntla', 'intu', 'isrg', 'nvta', 'irdm', 'jd', 'jpm', 'jnj', 'jmia', 'khc', 'lmnd', ' lmt', 'logi', 'lulu', 'lyft', 'mp', 'ma', 'mtch', 'maxr', 'mcd', 'mdla', 'meli', 'mstr', 'mu', 'msft', 'mrna', 'mdb', 'nndm', 'nflx', 'nee', 'nke', 'ntdoy', 'nio', 'niu', 'ntnx', 'nvda', 'okta', 'open', 'orcl', 'pacb', 'pd', 'pltr', 'pypl', 'payc', 'pton', 'penn', 'pep', 'pfe', 'pdd', 'pins', 'plnhf', 'plug', 'pg', 'prlb', 'pstg', 'qcom', 'rdfn', 'rvlv', 'hood', 'rblx', 'rkt', 'roku', 'sap', 'crm', 'sdgr', 'se', 'now', 'shak', 'shop', 'sklz', 'swks', 'work', 'snap', 'snow', 'sedg', 'sono', 'sony', 'luv', 'splk', 'spot', 'sq', 'sqsp', 'stmp', 'sbux', 'sfix', 'ssys', 'spwr', 'run', 'swch', 'tmus', 'tsm', 'ttwo', 'tgt', 'ttcf', 'tdoc', 'tcehy', 'ter', 'tsla', 'ttd', 'tlry', 'tm', 'twlo', 'twst', 'twtr', 'uber', 'u', 'upst', 'upwk', 'veev', 'vz', 'spce', ' v', 'wmt', 'w', 'wfc', 'wish', 'wix', 'wday', 'wkhs', 'xiacf', 'xpev', 'zen', 'z', 'zm', 'zs', 'ebay', 'fubo', 'irbt']

	# Berkshire B had . instead of "-""
	resolved_hyper = ["BRK-B"]	
	# Nitendo - ntdoy quoted in Japan
	# Plnhf - Canadian cannabis firm.
	# Xiaomi Corporation (XIACF) - could be Chinese

	sec_urls = [BASE_SEC_XML + symb for symb in all_hyper]	
	
	json_array = []
	
	headers = {'User-agent': 'Mozilla/5.0'}
	for url in sec_urls:
		try: 
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
		except:
			print("URL did not work:", url)
			continue
	
	with open('python_data/all_hyper.json', 'w') as outfile:
		json.dump(json_array, outfile)

get_xml()

