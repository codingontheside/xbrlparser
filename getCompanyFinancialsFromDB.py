from daoRefactor2 import DAO
from rssTickerInfo import rssTickerInfo
import json
import boto3
from FinancialValue import FinancialValue
from Financials import Financials
from stockScreen import stockScreen
import pandas as pd
import operator

table = 'FinancialValues'
stockPriceTable = 'TickerValue'
dao = DAO(table)
dao2 = DAO(stockPriceTable)

def listCompare(annual_list, annual_label, current_list, current_label):
	compare = operator.eq(annual_label, current_label)
	if  compare == True:
		return
	else:
		i = 0
		while i < len(annual_label):
			if annual_label[i] == current_label[i]:
				i += 1
				continue
			else:
				#annual_label.insert(i,current_label[i])
				print (annual_label[i])
				print(current_label[i])
				i +=1
				continue
	return 

def main():
	ticker = 'VLO'
	#print(ticker)
	tickerValues = dao.getCompanyFinancialValueDates(ticker)
	print(tickerValues)
	stockPrice = dao2.getTickerValue(ticker)[0]['StockPrice']
	print(stockPrice)
	fv = FinancialValue(ticker)
	annual_dict = {}
	quarterly_dict = {}
	values_annual_label = []
	values_annual_label_list = []
	values_annual_value_list = []
	values_annual_value = []
	values_quarterly_label = []
	values_quarterly_value = []
	for year in tickerValues:
		reportedDateAnnual = {}
		reportedDateQuarter = {}
		yearValues = dao.getCompanyFinancialValues(ticker, year['ReportedDate'])
		if yearValues[0]['FormType'] == '10-K':
			values_annual_value.append(year['ReportedDate'])
			values_annual_label.append('ReportedDate')
		elif yearValues[0]['FormType'] == '10-Q':
			values_quarterly_value.append(year['ReportedDate'])
			values_quarterly_label.append('ReportedDate')
		for key, values in yearValues[0]['financials'].items():
			fvalues = Financials(key,values, yearValues[0]['FormType'], year['ReportedDate'])
			if fvalues.filingPeriod == 'Annual':
				values_annual_label.append(fvalues.name)
				values_annual_value.append(fvalues.value)
				reportedDateAnnual[fvalues.name] = fvalues.value
			elif fvalues.filingPeriod == 'Quarter':
				values_quarterly_label.append(fvalues.name)
				values_quarterly_value.append(fvalues.value)
				reportedDateQuarter[fvalues.name] = fvalues.value
			elif fvalues.reportType == '10-K':
				values_annual_label.append(fvalues.name)
				values_annual_value.append(fvalues.value)
				reportedDateAnnual[fvalues.name] = fvalues.value
			elif fvalues.reportType == '10-Q':
				values_quarterly_label.append(fvalues.name)
				values_quarterly_value.append(fvalues.value)
				reportedDateQuarter[fvalues.name] = fvalues.value											
			#print(fvalues.name, fvalues.value, fvalues.filingPeriod, fvalues.reportType)
		annual_dict[year['ReportedDate']] = reportedDateAnnual
		quarterly_dict[year['ReportedDate']] = reportedDateQuarter
		if len(values_annual_value) > 0:
			updated_annual_label = listCompare(values_annual_value_list, values_annual_label_list, tuple(values_annual_value), values_annual_label)
			values_annual_value_list.append(tuple(values_annual_value))
			values_annual_value = [tuple(values_annual_value)]
		#stockdf = pd.DataFrame.from_records(values_annual_value, columns=values_annual_label, index='ReportedDate')
		#print(values_annual_label)
		#print(stockdf)
		if len(values_annual_label) > len(values_annual_label_list):
			values_annual_label_list = values_annual_label
			print('made it here')
		values_annual_label = []
		values_annual_value = []
		ssResults = stockScreen(year['ReportedDate'], yearValues[0]['financials'], stockPrice)
		print(ssResults.reportingPeriod)
		print(ssResults.earningsPerShare)
		print(ssResults.dividendRatio)
		print(ssResults.currentRatio)
	#print(value_annual)
	#print(value_quarter)
	print(annual_dict)
	print(quarterly_dict)
	#stockdf2 = pd.DataFrame.from_records(values_annual_value_list, columns=values_annual_label_list, index='ReportedDate')
	stockdf2 = pd.DataFrame.from_dict(annual_dict, orient = 'index')
	print(stockdf2)
		#print(yearValues[0])
		#df2 = pd.DataFrame({'Assets Current' : yearValues[0]['financials']['AssetsCurrent']['value'], 'Liabilities Current': yearValues[0]['financials']['LiabilitiesCurrent']['value'], 'Earnings Per Share Basic': yearValues[0]['financials']['EarningsPerShareBasic']['value']}, index = [year['ReportedDate']])
		#stockdf.append(df2)
		#print(ssResults.reportingPeriod)
	
		#print(ssResults.earningsPerShare)
		#print(ssResults.dividendRatio)
		#for key in year.get('financials'):
			#print(key)
		#print(year.get('financials').get('AssetsCurrent').get('value'))
	#print(stockdf)
if __name__ == "__main__": 
  
    # calling main function 
	    main()		