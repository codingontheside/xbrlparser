#! /usr/bin/env python
# encoding: utf-8

import feedparser
import urllib
from lxml import etree as ET
import re, urllib.request
import json
from datetime import datetime as DT
from initialVariables import financials_list

#import xml.etree.ElementTree as ET

def gatherURL():
	RSScontents = urllib.request.urlopen("https://www.sec.gov/Archives/edgar/usgaap.rss.xml", )
	#RSScontents = urllib.request.urlopen("https://www.sec.gov/Archives/edgar/data/27419/000110465910046222/tgt-20100731.xml",)
	RSStree = ET.parse(RSScontents)
	# get root elememen 
	RSSroot = RSStree.getroot()

	URLset = []
	companyInfo = {}

	formType = []
	x = 0
	y = 0

	for rootchild in RSSroot.iter('{http://www.sec.gov/Archives/edgar}xbrlFiling'):
		companyValues = {}
		companyValues['URL'] = 'Empty'
		companyName = None
		for rootchild2 in rootchild.iter('{http://www.sec.gov/Archives/edgar}companyName','{http://www.sec.gov/Archives/edgar}formType','{http://www.sec.gov/Archives/edgar}filingDate', '{http://www.sec.gov/Archives/edgar}cikNumber','{http://www.sec.gov/Archives/edgar}period','{http://www.sec.gov/Archives/edgar}fiscalYearEnd','{http://www.sec.gov/Archives/edgar}xbrlFile'):
			if rootchild2.tag == '{http://www.sec.gov/Archives/edgar}formType':
				companyValues['FormType'] = rootchild2.text
			elif rootchild2.tag == '{http://www.sec.gov/Archives/edgar}filingDate':
				companyValues['FilingDate'] = rootchild2.text
			elif rootchild2.tag == '{http://www.sec.gov/Archives/edgar}cikNumber':
				companyValues['CIKNumber'] = rootchild2.text
			elif rootchild2.tag == '{http://www.sec.gov/Archives/edgar}period':
				companyValues['Period'] = rootchild2.text
			elif rootchild2.tag == '{http://www.sec.gov/Archives/edgar}fiscalYearEnd':
				companyValues['FiscalYearEnd'] = rootchild2.text
			elif rootchild2.tag == '{http://www.sec.gov/Archives/edgar}companyName':
				companyName = rootchild2.text		
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
			companyInfo[companyName] = companyValues

	
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

def parseXML(perioddate, xmlfile):
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
	periodValues = {}
	dateValues = {}

	try:
		for context_tag in context_tags:
			# we don't want any segments
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
						else:
							try:
								if(context_tag.find(doc_root + "period").find(doc_root + "endDate")) is None:
									key_values.append(context_id + ',' + context_tag.find(doc_root + "period").find(doc_root + "startDate").text + ',' + ' ')
								else:
									key_values.append(context_id + ',' + context_tag.find(doc_root + "period").find(doc_root + "startDate").text + ',' + context_tag.find(doc_root + "period").find(doc_root + "endDate").text)
								#print(key_values[context_ids_size])
							except:
								continue	
					except:
						print('exception')
					context_ids_size = context_ids_size + 1
				else:
					continue

	except IndexError:
		raise XBRLParserException('problem getting contexts')
	financialValues = []
	#ValuesWeCareAbout = ['NetIncomeLoss', 'ProfitLoss', 'EarningsPerShareBasic','AssetsCurrent','LiabilitiesCurrent', 'CommonStockDividendsPerShareDeclared','CommonStockSharesOutstanding']
	for x in financials_list:
		startDatesize = 0
		category = []
		categoryValues = []
		for j in context_ids:
			#print(startDatesize)
			try:
				for child in root.iter(us_gaap_root + x):
					context = child.attrib.get('contextRef')
					#print(child)
					if context == j:
						try:
							y = key_values[startDatesize]
							context_id2,startDate,endDate =  y.split(',')
						except:
							startDate = 'none found'
							endDate = 'none found'
						#categoryValues.append(["Value:"+child.text,"StartDate:"+startDate,"EndDate:"+endDate])
						newStartDate = DT.strptime(startDate, '%Y-%m-%d')
						newEndDate = DT.strptime(endDate, '%Y-%m-%d')
						dateDiff = newEndDate - newStartDate
						if dateDiff.days < 100:
							if endDate == closingdate:
								periodValues[x] = child.text
								dateValues[endDate] = periodValues
							else:
								continue
						else:
							continue			

						#financialValues.append([x,child.text,startDate,endDate])
						#print(x + " is = " + child.text + ' : ' +  startDate + ' : ' + endDate)
			except:
				print('some sort of error' + xmlfile)
			startDatesize = startDatesize + 1
			#print(startDatesize)
		category.append([x,categoryValues])	
		financialValues.append([category])
	return[financialValues,dateValues];	

def Convert(tup, di): 
    di = dict(tup) 
    return di 

def main():

	#financial_data = parseXML(XMLfile)
	financial_data = {}
	#financial_data= gatherURL()
	financial_data = {"LINDSAY CORP": {
        "FormType": "10-Q",
        "FilingDate": "01/09/2019",
        "CIKNumber": "0000836157",
        "Period": "20181130",
        "URL": "http://www.sec.gov/Archives/edgar/data/836157/000156459019000460/lnn-20181130.xml"}}
	#financial_data = [(['TARGET CORP', '10-Q', '08/27/2010', '0000027419', '20100731'], 'https://www.sec.gov/Archives/edgar/data/27419/000110465910046222/tgt-20100731.xml')]
	fullReport = {}
	for key, values in financial_data.items():
		#print('This is the URL:')
		#print(x)
		if values['FormType'] == '10-Q':
			w = DT.strptime(values['Period'], "%Y%m%d")
			v = DT.date(w)
			z = str(values['URL'])
			symbol = {}
			symbol['FormType'] = values['FormType']
			symbol['ReportDate'] = values['FilingDate']
			symbol['AIC'] = values['CIKNumber']
			symbol['PeriodEnd'] = values['Period']
			symbol['XBRL URL'] = values['URL']
			#print(z)
			if z == 'Empty':
			#XMLfile = fetchXML(z)
	# 		#print(XMLfile)
	# 		#print(x[0])
				companyReturns = [values,'None']
			else:
				companyReturns = parseXML(v,z)
			symbol['Financials'] = companyReturns[1]

			fullReport[key] = symbol

			prettyjson = fullReport
			json_str = json.dumps(prettyjson, indent=4, sort_keys = False)
			#print(json_str)
	# 		#fullReport.append([x[0],x[1],companyReturns])
		else:
			continue	
	prettyjson = fullReport
	json_str = json.dumps(prettyjson, indent=4, sort_keys = False)
	print(json_str)

	#print(fullReport)	


if __name__ == "__main__": 
  
    # calling main function 
	    main()
