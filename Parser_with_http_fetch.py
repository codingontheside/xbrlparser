#! /usr/bin/env python
# encoding: utf-8

from lxml import etree as ET
import re, urllib.request

#import xml.etree.ElementTree as ET

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

def parseXML(xmlfile):
    # create element tree object 
	tree = ET.parse(xmlfile)
    # get root elememen 
	root = tree.getroot()

	root_values = find_root_values(tree)
	us_gaap_root = root_values[0]
	doc_root = root_values[1]

	context_ids = []
	key_values = []
	context_ids_size = 0
	context_tags = root.findall(doc_root +'context')

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

	ValuesWeCareAbout = ['NetIncomeLoss','EarningsPerShareBasic','AssetsCurrent','LiabilitiesCurrent']
	for x in ValuesWeCareAbout:
		#print(startDatesize)
		startDatesize = 0
		#print('now checkcing for ' + x)
		#print (len(context_ids))
		#print(context_ids)
		#print (len(key_values))
		#print(key_values)
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
						print(x + " is = " + child.text + ' : ' +  startDate + ' : ' + endDate)
			except:
				print('some sort of error')
			startDatesize = startDatesize + 1
			#print(startDatesize)

def main():
	print('This is the data for AAPL')
	financial_data = parseXML('./aapl-20150627.xml')
	print('This is the data for UNP')
	financial_data = parseXML('./UNP.xml')
	print('This is the data for Nike')
	financial_data = parseXML('./nke-20180831.xml')
	print('This is fetched data')
	XMLfile = fetchXML('http://www.sec.gov/Archives/edgar/data/1543739/000107878218001443/apty-20181031.xml')[0]
	financial_data = parseXML(XMLfile)

if __name__ == "__main__": 
  
    # calling main function 
	    main()
