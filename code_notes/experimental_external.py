@flask_app.route('/tickers', methods=['GET', 'POST'])
def ticker_data():
	with open('data/premium/stocks/prod/subset.json') as tickers_file:
		py_data = json.load(tickers_file)
		return jsonify(py_data)