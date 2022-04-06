from xmlrpc.client import boolean
from pycoingecko import CoinGeckoAPI
import json

cg = CoinGeckoAPI()	
all_coins = cg.get_coins_list(include_platform=False)

with open('all_coins_list.json', 'w') as outfile:
	json.dump(all_coins, outfile, indent=4)