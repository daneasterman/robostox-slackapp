dict = {
    "alert_nickname": "My Morgan Stanley Alert",
    "sec_source": "https://www.sec.gov/Archives/edgar/data/67088/000089924320008941/0000899243-20-008941-index.htm",
    "filed_at": "2020-52-18 20:03:47",
    "form": "4",
    "form_description": "Statement of changes in beneficial ownership of securities",
    "ticker": "MUFG",
    "ticker_company": "Mitsubishi UFJ Financial Group, Inc. Common Stock",
    "ticker_source": "https://finance.yahoo.com/quote/MUFG?p=MUFG&.tsrc=fin-srch",
    "exchange": "NYSE",
    "filers": {
        "6422": {
            "type": "reporting",
            "name": "MITSUBISHI UFJ FINANCIAL GROUP INC",
            "source": "https://www.sec.gov/cgi-bin/browse-edgar?CIK=67088&action=getcompany"
        },
        "311": {
            "type": "issuer",
            "name": "MORGAN STANLEY",
            "source": "https://www.sec.gov/cgi-bin/browse-edgar?CIK=895421&action=getcompany"
        }
    },
    "industries": [
        "Asset - Backed Securities"
    ]
}

ticker_list = ["MSFT", "TSLA", "AAPL", "MUFG"]

for t in ticker_list:
	if t in dict.values():
		print(f"TRUE, ticker {t} found in dict, full company name is: {dict['ticker_company']}")
	# else:
	# 	print(f"FALSE: ticker value {t} not found")








