from ParserRefactor2 import XbrlInfo as XI
from daoRefactor2 import DAO
from rssTickerInfo import rssTickerInfo
import json

rssValues = DAO('CompanyRSSFeed')
fvValues = DAO('FinancialValues')

def main():
	tickerValuesList = rssValues.getRssTickerValues('DPZ')
	for tickerValues in tickerValuesList:
		#print(tickerValues)
		tickerinfo = rssTickerInfo(tickerValues.get('Ticker'), tickerValues.get('url'), tickerValues.get('Date'), tickerValues.get('formType'), tickerValues.get('period'), tickerValues.get('fiscalYearEnd'))
		fv = XI(tickerinfo.URL, fvValues, tickerinfo.ticker, tickerinfo.period)
		financials = fv.getXBRLvalues()
		js_financials = json.dumps(financials, sort_keys = True, indent = 2)
		fvValues.setTickerFV(tickerinfo, financials)
		print(tickerinfo.ticker, tickerinfo.period, tickerinfo.URL, js_financials)


if __name__ == "__main__": 
    # calling main function 
	    main()		