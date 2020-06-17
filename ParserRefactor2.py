#! /usr/bin/env python
# encoding: utf-8


from lxml import etree as ET
import re, urllib.request
import urllib
import FinancialValue
from financialValuesName import financials_list, financials_names


class XbrlInfo():


	def __init__(self, URL, dao, ticker, closingDate):
		self.URL = URL
		self.financialValues = {}
		self.dao1 = dao
		self.ticker = ticker
		self.adjustClosingDate(closingDate)


	def loadXML(self):
		"This takes in an XML file and returns the root values"
		RSScontents = urllib.request.urlopen(self.URL, )
		RSStree = ET.parse(RSScontents)
		RSSroot = RSStree.getroot()
		return RSSroot

	def tagsplit(self, tag, position):
		"This splits an XML tag into the URL and the element"
		tempstring = tag.split('}')[position]
		return tempstring


	def adjustClosingDate(self, originalClosingDate):
		self.closingDate = originalClosingDate[0:4] + '-' + originalClosingDate[4:6] + '-' + originalClosingDate[6:8]


	def buildcd(self, contextd, child):
		"Takes in an element and updates the context dictionary"
		contexttags = {}
		for a in child.iter():
			tempstring = self.tagsplit(a.tag,1)
			if tempstring == 'period':
				for p in a:
					perioddate = self.tagsplit(p.tag,1)
					contexttags[perioddate] = str(p.text)
			elif tempstring == 'entity':
				for p in a:
					#print(self.tagsplit(p.tag,1))
					if self.tagsplit(p.tag,1) == 'segment':
						contexttags['segment'] = True
			contextd[child.attrib['id']] = contexttags
		return contextd;		

	def getContextDict(self, file):
		"Passing in an XBRL file it will return the context dictionary"
		self.ContextFile = file
		contextdict = {}
		for rootchild in self.ContextFile.iter():
			if type(rootchild.tag)  == str:
				ns = self.tagsplit(str(rootchild.tag),0) + '}'
				nsname = self.tagsplit(rootchild.tag,1)
				if nsname == 'context':
					contextdict = self.buildcd(contextdict,rootchild)
		return contextdict;			

	def getXBRLvalues(self):
		"Fetches XBRL info from web and parses into a dictionary of values"
		xbrl = self.loadXML()
		contextdict = self.getContextDict(xbrl)
		fvlist = {}
		for rootchild in xbrl.iter():
			if type(rootchild.tag)  == str:
				ns = self.tagsplit(str(rootchild.tag),0) + '}'
				nsname = self.tagsplit(rootchild.tag,1)

				if ns == ('{' + rootchild.nsmap['us-gaap'] +'}'):
					c = {}
					c['value'] = rootchild.text
					c['period'] = rootchild.attrib['contextRef']
					self.financialValues[nsname] = c
					fv1 = FinancialValue.FinancialValue(self.ticker)
					fv1.name = nsname
					fv1.value = rootchild.text
					fv1.period = rootchild.attrib['contextRef']
					fv1.startDate = 'temp'
					fv1.endDate = 'temp'
					fv1.updateperiod(contextdict)
					#print(self.closingDate)
					#print(fv.name, fv.value, fv.instant, fv.startDate, fv.endDate)
					if fv1.name in financials_list:
						#print(fv.name + '\n')
						fv1.updatename(financials_names)
						if fv1.segment == False:
							if self.closingDate in [fv1.instant, fv1.endDate]:
								if fv1.instant == 'temp':
									fv1.getPeriod()
								fvlist.update({fv1.name : {'value' : fv1.value, 'instant' : fv1.instant, 'startDate': fv1.startDate, 'endDate': fv1.endDate, 'filingPeriod': fv1.filingPeriod}})
					#self.dao1.setTickerFV(fv)

		#self.financialValues = self.updateperiod(contextdict, self.financialValues) #replaces the contextRef with actual values
		return fvlist
