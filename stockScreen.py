#! /usr/bin/env python
# encoding: utf-8

class stockScreen():

	def __init__(self, reportedDate, financials, stockPrice):
		self.reportingPeriod = reportedDate
		self.stockPrice = stockPrice
		self.currentRatio = self.getCurrentRatio(financials)
		self.earningsPerShare = self.getPERatio(financials)
		self.dividendRatio = self.getDividendRatio(financials)



	def getCurrentRatio(self, financials):
		#print(financials)
		self.assetsCurrent = financials['AssetsCurrent']['value']
		self.debtCurrent = financials['LiabilitiesCurrent']['value']
		return (float(self.assetsCurrent) / float(self.debtCurrent))

	def getPERatio(self, financials):
		return(float(float(self.stockPrice) / float(financials['EarningsPerShareBasic']['value'])))

	def getDividendRatio(self, financials):
		if financials.get('CommonStockDividendsPerShareDeclared') != None:
			return(float(float(financials['CommonStockDividendsPerShareDeclared']['value']))/float(self.stockPrice))
		else:
			return '0'