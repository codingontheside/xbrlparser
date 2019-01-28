import json
from datetime import datetime as DT
from decimal import *
import simplejson as json

def getHistoricalFinancials(ticker,tickerDict):
	if ticker in tickerDict:
		tempkeyValue = tickerDict.get(ticker)
		tempFinancials = tempkeyValue.get('Financials')
	else:
		tempFinancials = {}
	return tempFinancials;

def getCurrentStockPrice(ticker,tickerDict):
	if ticker in tickerDict:
		tempkeyValue = tickerDict.get(ticker)
		tempStockPrice = tempkeyValue.get('ClosingPrice')
	else:
		tempStockPrice = 0.0
	return tempStockPrice;	

def getEarningsGrowth(historicalF):
	a = getAnnualEarnings('Annual:', 'EarningsPerShareBasic', historicalF)
	if len(a) > 0:
		periods = a.keys()
		oldest = min(periods)
		newest = max(periods)
	#dateRange = newest - oldest
		if oldest != newest:
			try:
				growth = Decimal(Decimal(a[newest]) / Decimal(a[oldest])) - Decimal(1.0)
			except ZeroDivisionError:
				growth = None	
		elif oldest == newest:
			growth = None
	else:
		growth = None		
	return(growth,len(a));

def getDividendRecord(historicalF):
	a = getAnnualEarnings('Annual:', 'CommonStockDividendsPerShareDeclared',historicalF)
	dividendPaid = 0
	continuousDividends = False
	if len(a) > 0:
		periods = a.keys()
		oldest = min(periods)
		oldestDate = DT.strptime(oldest, '%Y-%m-%d')
		newest = max(periods)
		newestDate = DT.strptime(newest, '%Y-%m-%d')
		yearsDiff = newestDate.year - oldestDate.year
		#print('YearsDiff:')
		#print(yearsDiff)
		for key, keyvalue in a.items():
			keyvalueInt = float(keyvalue)
			if keyvalueInt > 0.0:
				dividendPaid = dividendPaid + 1
			else:
				continue
		#print('DividentPaid:')
		#print(dividendPaid)
		if dividendPaid < yearsDiff:
			continuousDividends = False
		else:
			continuousDividends = True
	return continuousDividends;		

def getCurrentPEratio(stockPrice,historicalF):
	a = getAnnualEarnings('Annual:', 'EarningsPerShareBasic', historicalF)
	averageAnnualEarnings = 0.0
	if len(a) > 0:
		earnings = 0.0
		for key, keyvalue in a.items():
			earnings = float(keyvalue) + earnings
		averageAnnualEarnings = earnings / len(a)	
	else:
		pass
	if averageAnnualEarnings != 0.0:
		currentPEratio = stockPrice / averageAnnualEarnings
	else:
		currentPEratio = 'N/A'
	return currentPEratio;	


def getCurrentRatio(historicalF):
	a = getAnnualEarnings('As of:', 'AssetsCurrent', historicalF)
	b = getAnnualEarnings('As of:', 'LiabilitiesCurrent', historicalF)
	if len(a) > 0 and len(b) > 0:
		periods_a = a.keys()
		current = max(periods_a)
		aValue = float(a[current])
		bValue = float(b[current])
		currentRatio = float(aValue / bValue)
	else:
		currentRatio = 0.0
	return(currentRatio)	


def getAnnualEarnings(period, financialtype, historicalF):
	earningsDict = {}
	if period in historicalF:
		annualKey = historicalF[period]
	else:
		return earningsDict;
	for key, keyvalue in annualKey.items():
		if financialtype in keyvalue:
			earnings = keyvalue[financialtype]	
			earningsDict.update({key:earnings})
		else:
			pass
	return earningsDict;			

def main():
	r = {}
	with open('DecemberFinancialData.json', 'r') as f:
		try:
			r = json.loads(f.read())
		except:
			pass
		finally:	
			f.close()
	if len(r) > 0:
		overallResults = {}
		for key in r:
			screenerResults = {}
			rr = getHistoricalFinancials(key,r)
			ss = getCurrentStockPrice(key,r)
			response = getEarningsGrowth(rr)
			screenerResults['Earnings Growth'] = response[0]
			screenerResults['Current Ratio'] = getCurrentRatio(rr)
			screenerResults['Dividend Record'] = getDividendRecord(rr)
			screenerResults['PE Ratio'] = getCurrentPEratio(ss,rr)
			growth = response[0]
			periods = response[1]
			growthrate = 0
			if growth != None:
				growthrate = (((1+float(growth) ** (1/(periods-1)))-1)*100)
				#print(type(growthrate))
				if type(growthrate) == complex:
					growthrate = 0.0
				screenerResults['Growth Rate'] = growthrate
			else:
				pass	
			overallResults[key] = screenerResults

	else:
		rr = {}		
	#print(overallResults)
	json_str = json.dumps(overallResults, indent=4, sort_keys = True, use_decimal = True)
	print(json_str)




if __name__ == "__main__": 
  
    # calling main function 
	    main()			