#! /usr/bin/env python
# encoding: utf-8

import csv
import feedparser
import urllib
from lxml import etree as ET
import re, urllib.request
import json
from datetime import datetime as DT
from initialVariables import financials_list

#import xml.etree.ElementTree as ET

def getHistoricalFinancials(ticker,tickerDict):
	if ticker in tickerDict:
		tempkeyValue = tickerDict.get(ticker)
		tempFinancials = tempkeyValue.get('Financials')
	else:
		tempFinancials = {}
	return tempFinancials;


def updateDict(ultparentdict, ultparentkey, parentkey, childkey, childvalue):
	if ultparentkey in ultparentdict:
		parentdict = ultparentdict[ultparentkey]
	else:
		parentdict = {}	
	if parentkey in parentdict:
		childdict = parentdict[parentkey]
	else:
		childdict = {}
	childdict.update({childkey:childvalue})
	parentdict.update({parentkey:childdict})
	ultparentdict.update({ultparentkey:parentdict})
	return ultparentdict, parentdict, childdict;


def getStockPrice(ticker):
	tickerPrice = 'None'
	try:
		fetchURL = 'https://api.iextrading.com/1.0/stock/' + ticker + '/quote'
		contents = urllib.request.urlopen(fetchURL, ).read().decode('utf-8')
		json_obj = json.loads(contents)
		#print(json_obj)
		tickerPrice = json_obj['latestPrice']
	except:
		if tickerPrice == 'None':
			tickerPrice = 'N/A'
	return tickerPrice;

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
				stockList[row['Symbol']] = key
	return stockList;			

def gatherURL(companyListvar):
	#RSScontents = urllib.request.urlopen("https://www.sec.gov/Archives/edgar/usgaap.rss.xml", )
	RSScontents = urllib.request.urlopen('https://www.sec.gov/Archives/edgar/monthly/xbrlrss-2018-12.xml', )
	RSStree = ET.parse(RSScontents)
	RSSroot = RSStree.getroot()
	companyInfo = {}

	for rootchild in RSSroot.iter('{http://www.sec.gov/Archives/edgar}xbrlFiling'):
		companyValues = {}
		companyValues['URL'] = 'Empty'
		companyValues['Ticker'] = 'Empty'
		companyName = None
		companyTicker = None
		for rootchild2 in rootchild.iter('{http://www.sec.gov/Archives/edgar}companyName','{http://www.sec.gov/Archives/edgar}formType','{http://www.sec.gov/Archives/edgar}filingDate', '{http://www.sec.gov/Archives/edgar}cikNumber','{http://www.sec.gov/Archives/edgar}period','{http://www.sec.gov/Archives/edgar}fiscalYearEnd','{http://www.sec.gov/Archives/edgar}xbrlFile','{http://www.sec.gov/Archives/edgar}acceptanceDatetime'):
			if rootchild2.tag == '{http://www.sec.gov/Archives/edgar}formType':
				companyValues['FormType'] = rootchild2.text
			elif rootchild2.tag == '{http://www.sec.gov/Archives/edgar}filingDate':
				companyValues['FilingDate'] = rootchild2.text
			elif rootchild2.tag == '{http://www.sec.gov/Archives/edgar}cikNumber':
				companyValues['CIKNumber'] = rootchild2.text
			elif rootchild2.tag == '{http://www.sec.gov/Archives/edgar}period':
				companyValues['Period'] = rootchild2.text
			elif rootchild2.tag == '{http://www.sec.gov/Archives/edgar}acceptanceDatetime':
				companyValues['AcceptanceDate'] = rootchild2.text	
			elif rootchild2.tag == '{http://www.sec.gov/Archives/edgar}fiscalYearEnd':
				companyValues['FiscalYearEnd'] = rootchild2.text
			elif rootchild2.tag == '{http://www.sec.gov/Archives/edgar}companyName':
				companyValues['companyName'] = rootchild2.text		
			elif rootchild2.tag == '{http://www.sec.gov/Archives/edgar}xbrlFile':
					description = rootchild2.attrib.get('{http://www.sec.gov/Archives/edgar}description')
					if description == 'XBRL INSTANCE DOCUMENT':
						companyValues['URL'] = rootchild2.attrib.get('{http://www.sec.gov/Archives/edgar}url')
					elif description == 'EX-101.INS':
						companyValues['URL'] = rootchild2.attrib.get('{http://www.sec.gov/Archives/edgar}url')
					elif description == 'XBRL FILE; INSTANCE':
						companyValues['URL'] = rootchild2.attrib.get('{http://www.sec.gov/Archives/edgar}url')
					elif description == 'XBRL INSTANCE FILE':
						companyValues['URL'] = rootchild2.attrib.get('{http://www.sec.gov/Archives/edgar}url')		
					else:
						continue
					tickerFindList = companyValues['URL'].split('/')
					tickerFindListSize = len(tickerFindList)
					tickerFindString = tickerFindList[tickerFindListSize-1]
					tickerFindStringSplit = tickerFindString.split('-')
					companyTicker = tickerFindStringSplit[0].upper()
		#print(companyValues['Ticker'])
		if  companyTicker in companyListvar:
			companyInfo[companyTicker] = companyValues
		else:
			continue
	
	#print(URLset)
	return companyInfo;


def fetchXML(URL):
	"will fetch the an MMRL file from a URL"
	contents = urllib.request.urlopen(URL, )
	return[contents];


def find_root_values(parsedxmlfile):
	"Returns the us_gaap_root value from an XML file"
	doc = parsedxmlfile
	nsmap = {}
	us_gaap_root = None
	doc_root = None
	for ns in doc.xpath('//namespace::*'):
		if ns[0]:
			nsmap[ns[0]] = ns[1]
			ns1= ns[0]
			ns2 = ns[1]
			if ns1 == 'us-gaap':
				us_gaap_root = ns2
			elif ns1 == 'xbrli':
				doc_root = ns2
	if doc_root == None:
		doc_root = 	doc_root = '{http://www.xbrl.org/2003/instance}'
	else:
		doc_root =  '{' + doc_root + '}'
	if us_gaap_root == None:
		us_gaap_root = '{http://fasb.org/us-gaap/2018-01-31}'
	else:
		us_gaap_root = '{' + us_gaap_root + '}'
	#print (us_gaap_root)
	return [us_gaap_root,doc_root];

def parseXML(perioddate, xmlfile,historicalF):
    # create element tree object 
	contents = urllib.request.urlopen(xmlfile, )
	tree = ET.parse(contents)
    # get root elememen 
	root = tree.getroot()

	root_values = find_root_values(tree)
	us_gaap_root = root_values[0]
	doc_root = root_values[1]
	closingdate = str(perioddate)
	context_ids = []
	key_values = []
	context_ids_size = 0
	context_tags = root.findall(doc_root +'context')
	context_dict = {}
	periodValues = {}
	instantValues = {}
	dateValues = {}
	ultimateDateValues = historicalF

	try:
		for context_tag in context_tags:
			# we don't want any segments
			context_date_dict = {}
			if context_tag.find(doc_root + "entity") is None:
				continue
			else:
				if context_tag.find(doc_root + "entity").find(doc_root + "segment") is None:
					
					
					context_id = context_tag.attrib['id']
					
					#print(context_tag.attrib['id'])
					context_ids.append(context_id)
					try:
						if (context_tag.find(doc_root + "period").find(doc_root + "instant")) != None:
							key_values.append(context_id + ',' + context_tag.find(doc_root + "period").find(doc_root + "instant").text + ',' + context_tag.find(doc_root + "period").find(doc_root + "instant").text)
							context_date_dict['instant'] = context_tag.find(doc_root + "period").find(doc_root + "instant").text
							context_date_dict['startDate'] = None
							context_date_dict['endDate'] = None
						else:
							context_date_dict['instant'] = None
							try:
								if(context_tag.find(doc_root + "period").find(doc_root + "endDate")) is None:
									key_values.append(context_id + ',' + context_tag.find(doc_root + "period").find(doc_root + "startDate").text + ',' + ' ')
									context_date_dict['startDate'] = context_tag.find(doc_root + "period").find(doc_root + "startDate").text
									context_date_dict['endDate'] = ''
								else:
									key_values.append(context_id + ',' + context_tag.find(doc_root + "period").find(doc_root + "startDate").text + ',' + context_tag.find(doc_root + "period").find(doc_root + "endDate").text)
									context_date_dict['startDate'] = context_tag.find(doc_root + "period").find(doc_root + "startDate").text
									context_date_dict['endDate'] = context_tag.find(doc_root + "period").find(doc_root + "endDate").text
								#print(key_values[context_ids_size])
							except:
								continue	
					except:
						print('exception')
					context_ids_size = context_ids_size + 1
					context_dict[context_id] = context_date_dict

				else:
					continue

	except IndexError:
		raise XBRLParserException('problem getting contexts')
	financialValues = []
	#json_str2 = json.dumps(context_dict, indent=4, sort_keys = False)
	#print(json_str2)
	#ValuesWeCareAbout = ['NetIncomeLoss', 'ProfitLoss', 'EarningsPerShareBasic','AssetsCurrent','LiabilitiesCurrent', 'CommonStockDividendsPerShareDeclared','CommonStockSharesOutstanding']
	for x in financials_list:
		startDatesize = 0
		
		category = []
		categoryValues = []
		for child in root.iter(us_gaap_root + x):
			j_value = context_dict.get(child.attrib.get('contextRef'))
			try:
				instant = j_value['instant']
			except:
				continue	
			try:
				startDate = j_value['startDate']
			except:
				continue	
			try:
				endDate = j_value['endDate']
			except:
				continue
			if instant != None:
				try:
					newInstantDate = DT.strptime(instant, '%Y-%m-%d')
				except:
					newInstantDate = DT.now()	
			if startDate != None:
				try:
					newStartDate = DT.strptime(startDate, '%Y-%m-%d')
				except:
					newStartDate = DT.now()
			else:
				newStartDate = DT.now()
			if endDate != None:
				try:
					newEndDate = DT.strptime(endDate, '%Y-%m-%d')
				except:
					newEndDate = DT.now()	
			else: 
				newEndDate = DT.now()
			dateDiff = newEndDate - newStartDate
			#print(dateDiff.days)
			if instant != None:
				updateDictValues = updateDict(ultimateDateValues, 'As of:', instant,x,child.text)
				ultimateDateValues = updateDictValues[0]
				dateValues = updateDictValues[1]

				#instantValues = updateDictValues[1]
			if dateDiff.days > 1 and dateDiff.days < 100:
				updateDictValues = updateDict(ultimateDateValues, 'Quarterly', endDate,x,child.text)
				ultimateDateValues = updateDictValues[0]
				dateValues = updateDictValues[1]
			elif dateDiff.days > 360 and dateDiff.days < 370:
				updateDictValues = updateDict(ultimateDateValues, 'Annual:', endDate,x,child.text)
				ultimateDateValues = updateDictValues[0]
				dateValues = updateDictValues[1]
				#periodValues = updateDictValues[1]
			else:
				continue	

		category.append([x,categoryValues])	
		financialValues.append([category])
	return[financialValues,ultimateDateValues];

def Convert(tup, di): 
    di = dict(tup) 
    return di 

def main():

	#financial_data = parseXML(XMLfile)
	r = {}
	with open('latestFinancialData.json', 'r') as f:
		try:
			r = json.loads(f.read())
		except:
			pass
		finally:	
			f.close()
	companyList = getTickerMarkets()
	financial_data = {}
	financial_data= gatherURL(companyList)
	#financial_data = {"LINDSAY CORP": {
        # "FormType": "10-Q",
        # "FilingDate": "01/09/2019",
        # "CIKNumber": "0000836157",
        # "Period": "20181130",
        # "URL": "http://www.sec.gov/Archives/edgar/data/836157/000156459019000460/lnn-20181130.xml"}}
	#financial_data = [(['TARGET CORP', '10-Q', '08/27/2010', '0000027419', '20100731'], 'https://www.sec.gov/Archives/edgar/data/27419/000110465910046222/tgt-20100731.xml')]
	fullReport = {}
	#print(financial_data)
	for key, values in financial_data.items():
		#print('This is the URL:')
		#print(x)
		if len(r) > 0:
			rr = getHistoricalFinancials(key,r)
		else:
			rr = {}	
		a = DT.strptime(values['AcceptanceDate'], "%Y%m%d%H%M%S")
		datediff = DT.today() - a
		if datediff.days < 40:
			#print(a)
			if values['FormType'] == '10-K' or values['FormType'] == '10-Q':
				w = DT.strptime(values['Period'], "%Y%m%d")
				v = DT.date(w)
				z = str(values['URL'])
				symbol = {}
				symbol['FormType'] = values['FormType']
				symbol['ReportDate'] = values['FilingDate']
				symbol['AIC'] = values['CIKNumber']
				symbol['PeriodEnd'] = values['Period']
				symbol['XBRL URL'] = values['URL']
				symbol['CompanyName'] = values['companyName']
				symbol['ClosingPrice'] = getStockPrice(key)
				#print(z)
				if z == 'Empty':
				#XMLfile = fetchXML(z)
	# 			#print(XMLfile)
	# 			#print(x[0])
					companyReturns = [values,'None']
				else:
					companyReturns = parseXML(v,z,rr)
				symbol['Financials'] = companyReturns[1]

				fullReport[key] = symbol

				prettyjson = fullReport
				json_str = json.dumps(prettyjson, indent=4, sort_keys = False)
				#print(json_str)
	# 			#fullReport.append([x[0],x[1],companyReturns])
			else:
				continue
		else:
			continue			
	prettyjson = fullReport
	with open('DecemberFinancialData.json', 'w') as f:
		json.dump(prettyjson, f, indent=4, sort_keys = True)
	#print(json_str)

	#print(fullReport)	


if __name__ == "__main__": 
  
    # calling main function 
	    main()
