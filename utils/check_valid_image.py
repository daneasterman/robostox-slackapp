from urllib.request import urlopen

def check_valid_image(url):
	image_formats = ("image/png", "image/jpeg", "image/jpg")	
	try:
		site = urlopen(url)
		meta = site.info()  # get header of the http request
		if meta["content-type"] in image_formats:
			return True
	except:
		return False
	