#! /usr/bin/env python
# encoding: utf-8


from lxml import etree as ET
import re, urllib.request
import urllib
from ParserRefactor2 import XbrlInfo as XI
from daoRefactor2 import DAO
from rssTickerInfo import rssTickerInfo
import json
import boto3

#localfile = 'https://www.sec.gov/Archives/edgar/monthly/xbrlrss-2019-10.xml'
localfile = 'file:///D:/Users/jesse/Projects/DataLoader/xbrlrss-2019-10.xml'
#dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
table = 'CompanyRSSFeed'
dao = DAO(table)
table2 = 'TickerList'
dao2 = DAO(table2)


def loadXML2(rssURL):
	"This takes in an XML file and returns the root values"
	RSScontents = urllib.request.urlopen(rssURL, )
	RSStree = ET.parse(RSScontents)
	RSSroot = RSStree.getroot()
	return RSSroot;

def findTicker(URL):
	tickerFindList = URL.split('/')
	tickerFindListSize = len(tickerFindList)
	tickerFindString = tickerFindList[tickerFindListSize-1]
	tickerFindStringSplit = tickerFindString.split('-')
	companyTicker = tickerFindStringSplit[0].upper()
	return companyTicker;

def tagsplit(tag, position):
	"This splits an XML tag into the URL and the element"
	tempstring = tag.split('}')[position]
	return tempstring;

def nsfind(tag):
	"This takes a tag and returns the namespace"
	ns = [0,1]
	ns[0] = tagsplit(tag,0) + '}'
	ns[1] = tagsplit(tag,1)
	return ns;

def filterxbrlfile(tag):
	"Filters out to only look for ULRs that might contain XBRL information"
	URLlist = ['XBRL INSTANCE DOCUMENT','EX-101.INS','XBRL FILE; INSTANCE','XBRL INSTANCE FILE', '10-Q']
	URL = None
	description = tag.attrib.get('{https://www.sec.gov/Archives/edgar}description')
	if description in URLlist:
		if description == '10-Q':
			URL = tag.attrib.get('{https://www.sec.gov/Archives/edgar}url')
			URL = URL[:-4]
			URL = URL + '_htm.xml'
		else:
			URL = tag.attrib.get('{https://www.sec.gov/Archives/edgar}url')
	return URL;

def processor(rssURL, TickerList):
	rssroot = loadXML2(rssURL)
	companydict = {}
	for child in rssroot.iter('{https://www.sec.gov/Archives/edgar}xbrlFiling'):
		singlecompany = {}
		for child2 in child.iter():
			elementname = nsfind(child2.tag)[1]
			if elementname == 'xbrlFile':
				#print(child2.tag, child2.attrib)
				URL = filterxbrlfile(child2)
				if URL != None:
					singlecompany['URL'] = URL
			else:
				singlecompany[elementname] = child2.text
		if 'URL' in singlecompany:
			companydict[findTicker(singlecompany['URL'])] = singlecompany
			companyRSS = rssTickerInfo(findTicker(singlecompany.get('URL')), singlecompany.get('URL'), singlecompany.get('filingDate'), singlecompany.get('formType'), singlecompany.get('period'), singlecompany.get('fiscalYearEnd'))
			if companyRSS.ticker == 'UNP': 
				print(companyRSS.ticker)
			if companyRSS.ticker in TickerList:
				if companyRSS.formType in ('10-Q'):
					#print(companyRSS.ticker, companyRSS.date, companyRSS.formType, companyRSS.URL)
					dao.setRssTickerValues(companyRSS)	
		
def main():
	#monthrange = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
	monthrange = ['09', '10', '11', '12']
	TickerDict = dao2.getTickerList()
	TickerList = []
	for child in TickerDict:
		TickerList.append(child['Ticker'])
	#print(TickerList)
	for month in monthrange:
		processor('https://www.sec.gov/Archives/edgar/monthly/xbrlrss-2019-' + month +'.xml', TickerList)

if __name__ == "__main__": 
  
    # calling main function 
	    main()		
