import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
from pycoingecko import CoinGeckoAPI
# db.collection(u'cities').document(u'LA').set(data)

cred = credentials.Certificate('firestore-sdk.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

cg = CoinGeckoAPI()	
# 1st bunny = 22
# 2nd bunny = 31
# START AT 1:
raw_coin_batch = cg.get_coins_markets(vs_currency="usd", 
	order="market_cap_desc", page=10)
coins_ref = db.collection("coins")

breakpoint()

for item in raw_coin_batch:	
	
	symbol_query = coins_ref.where("coin_symbol", "==", item["symbol"])
	symbol_results = symbol_query.get()	

	try:
		if symbol_results:
			db_coin_symbol = symbol_results[0].get("coin_symbol")
			db_coin_id = symbol_results[0].get("coin_id")

			print(f"NEW API: {item['symbol']} => {item['id']}")
			print(f"EXISTING DB: {db_coin_symbol} => {db_coin_id}\n")
			pass
		else:
			coins_ref.document(item["symbol"]).set({
				"coin_id": item["id"],
				"coin_symbol": item["symbol"],
				"coin_marketcap_rank": item["market_cap_rank"]
			})
	except Exception as e:
		print(f"Error when trying to add to Firestore DB: {e}")		
		break
	
	# List array must be outside for loop
	# bunny_page = []
	# bunny_page.append({
	# 	"api_symbol": api_symbol,
	# 	"api_coin_id": api_coin_id		
	# })
	# with open('json_data/bunny_page.json', 'w') as outfile:
	# 	json.dump(bunny_page, outfile, indent=4)