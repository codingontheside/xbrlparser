import boto3
from time import time
from boto3.dynamodb.conditions import Key, Attr

class DAO():

	def __init__(self, table):
		#self.session = session
		self.dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
		self.classtable = table
		self.table = self.dynamodb.Table(self.classtable)

	def setTickerFV(self, FV, financials):
		self.object = FV
		#print(self.object.ticker, self.object.name, self.object.value)
		response = self.table.put_item(
			Item={
				'Ticker' : str(self.object.ticker),
				'ReportedDate' : self.object.period,
				'FormType' : self.object.formType,
				'financials' : financials
				}
			)
	def setRssTickerValues(self, rss):	
		response = self.table.put_item(
			Item={
				'Ticker' : str(rss.ticker),
				'Date' : str(rss.date),
				'formType' : rss.formType,
				'url' : rss.URL,
				'period' : rss.period,
				'fiscalYearEnd' : rss.fiscalYearEnd
				}
			)

	def getRssTickerValues(self, ticker):

		dbresponse = self.table.query(
			KeyConditionExpression=Key('Ticker').eq(ticker)
		)
		tickerValues = dbresponse.get('Items')

		return tickerValues;		

	def setTickerList(self, ticker):
		response = self.table.put_item(
			Item={
				'Ticker' : ticker['symbol'],
				'StockPrice' : ticker['stockPrice']
			})	

	def getTickerList(self):
		response = self.table.scan()
		response = response.get('Items')
		return response

	def setTickerValue(self, ticker):
		response = self.table.put_item(
			Item={
				'Ticker' : ticker['symbol'],
				'StockPrice' : ticker['stockPrice']
			})

	def getTickerValue(self, ticker):
		response = self.table.query(
			KeyConditionExpression=Key('Ticker').eq(ticker)
			)
		tickerValue = response.get('Items')
		return tickerValue

	def getCompanyFinancialValueDates(self, ticker):

		dbresponse = self.table.query(
			ProjectionExpression='ReportedDate',
			KeyConditionExpression=Key('Ticker').eq(ticker)# & Key('ReportedDate').eq('20171231')
			)
		companyValues = dbresponse.get('Items')
		return companyValues

	def getCompanyFinancialValues(self, ticker, date):
		dbresponse = self.table.query(
			#ProjectionExpression='ReportedDate',
			KeyConditionExpression=Key('Ticker').eq(ticker) & Key('ReportedDate').eq(date)
			)
		companyValues = {}
		companyValues = dbresponse.get('Items')
		return companyValues
