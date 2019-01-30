import feedparser
import urllib
from lxml import etree as ET
import re
import csv
import json

def getTickerMarkets():
	stockList = {}
	exchangeList = {}
	exchangeList['NASDAQ'] = 'D:/Users/jesse/Downloads/NASDAQ.csv'
	exchangeList['AMEX'] = 'D:/Users/jesse/Downloads/AMEX.csv'
	exchangeList['NYSE'] = 'D:/Users/jesse/Downloads/NYSE.csv'
	for key, values in exchangeList.items():
		with open(values, newline = '') as csvfile:
			StockListcsv = csv.DictReader(csvfile)
			for row in StockListcsv:
				stockList[row['Symbol']] = {}
	return stockList;

def getStockPrice(ticker):
	tickerPrice = 'None'
	tickerDate = 'None'
	try:
		fetchURL = 'https://api.iextrading.com/1.0/stock/' + ticker + '/quote'
		#print(fetchURL)
		contents = urllib.request.urlopen(fetchURL, ).read().decode('utf-8')
		json_obj = json.loads(contents)
		#print(json_obj)
		tickerPrice = json_obj['latestPrice']
		tickerDate = json_obj['latestTime']
	except:
		if tickerPrice == 'None':
			tickerPrice = 'N/A'
	return [tickerDate, tickerPrice];

def main():
	r = {}
	# with open('stockPriceList.json', 'r') as f:
	# 	try:
	# 		r = json.loads(f.read())
	# 	except:
	# 		pass
	# 	finally:
	# 		f.close()
	r = getTickerMarkets()
	#print(r)
	for key, keyvalue in r.items():
		tempkey = {}
		todaysPrice = getStockPrice(key)
		#print(todaysPrice)
		tempkey[todaysPrice[0]] = todaysPrice[1]
		r[key] = tempkey
		print(key)
	json_obj = json.dumps(r,indent=4, sort_keys = True)
	with open('stockPriceListing.json', 'w') as f:
		json.dump(r, f, indent=4, sort_keys = True)


if __name__ == "__main__": 
  
    # calling main function 
	    main()		