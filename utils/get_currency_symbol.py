from .currency_symbols import CURRENCY_SYMBOLS_DICT

def get_currency_symbol(currency):
	if not currency:
		return ""
	else:
		return CURRENCY_SYMBOLS_DICT.get(currency)