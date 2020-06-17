from lxml import etree as ET
import re, urllib.request
import urllib
from daoRefactor2 import DAO
from decimal import *
import json

table = 'TickerValue'
dao = DAO(table)

def main():
	
	fetchURL = 'https://ws-api.iextrading.com/1.0/tops/last'
	topsResponse = urllib.request.urlopen(fetchURL, ).read().decode('utf-8')
	json_obj = json.loads(topsResponse)
	#print(json_obj)
	for company in json_obj:
		#if company.get('securityType') == 'commonstock':
		print(company.get('price'))
		if company.get('price') != None:
			tickerV = {}
			tickerV['symbol'] = company.get('symbol')
			tickerV['stockPrice'] = str(Decimal(company.get('price')).quantize(Decimal('.01'), rounding=ROUND_UP))
			print(tickerV)
			dao.setTickerValue(tickerV)
			#print(company.get('symbol'))

if __name__ == "__main__": 
  
    # calling main function 
	    main()			