#! /usr/bin/env python
# encoding: utf-8
from datetime import datetime


class FinancialValue():

	def updateperiod(self,context):
		"This replaces the reference ID with the actual value"
		tempdict = context[self.period]
		for childkey, childvalue in tempdict.items():
			#print(childkey, childvalue)
			setattr(self, childkey, childvalue)

	def getPeriod(self):
		endtime = datetime.strptime(self.endDate, "%Y-%m-%d")
		starttime = datetime.strptime(self.startDate, "%Y-%m-%d")
		daysdiff = endtime - starttime
		if daysdiff.days > 360:
			self.filingPeriod = 'Annual'
		else:
			self.filingPeriod = 'Quarter'

	def dosomething(self):
		print('made it here')

	def updatename(self, nameslist):
		self.name = nameslist[self.name]

	def __init__(self, ticker):
		self.ticker = ticker
		self.name = None
		self.value = None
		self.period = None
		self.startDate = 'temp'
		self.endDate = 'temp'
		self.instant = 'temp'
		self.segment = False
		self.filingPeriod = None
