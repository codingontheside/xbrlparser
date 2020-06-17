financials_list = ['GrossProfit','NetIncomeLoss',\
'Revenues','RevenueFromContractWithCustomerIncludingAssessedTax',\
'EarningsPerShareBasic','EarningsPerShareBasicAndDiluted',\
'AssetsCurrent',\
'LiabilitiesCurrent','LongTermDebtCurrent',\
'CommonStockDividendsPerShareDeclared','CommonStockDividendsPerShareCashPaid',\
'CommonStockSharesOutstanding', 'WeightedAverageNumberOfSharesOutstandingBasic','SharesOutstanding',\
'StockholdersEquity', 'ShareholderEquity','StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest']

financials_names = {
	'GrossProfit' : 'NetIncomeLoss',
	'NetIncomeLoss' : 'NetIncomeLoss',
	'Revenues' : 'Revenues',
	'RevenueFromContractWithCustomerIncludingAssessedTax' : 'Revenues',
	'EarningsPerShareBasic' : 'EarningsPerShareBasic',
	'EarningsPerShareBasicAndDiluted' : 'EarningsPerShareBasic',
	'AssetsCurrent' : 'AssetsCurrent',
	'CurrentAssets' : 'AssetsCurrent',
	'LiabilitiesCurrent' : 'LiabilitiesCurrent',
	'LongTermDebtCurrent' : 'LiabilitiesCurrent',
	'CommonStockDividendsPerShareDeclared' : 'CommonStockDividendsPerShareDeclared',
	'CommonStockDividendsPerShareCashPaid' : 'CommonStockDividendsPerShareDeclared',
	'CommonStockSharesOutstanding' : 'CommonStockSharesOutstanding',
	'SharesOutstanding' : 'CommonStockSharesOutstanding',
	'WeightedAverageNumberOfSharesOutstandingBasic' : 'CommonStockSharesOutstanding',
	'StockholdersEquity' : 'StockholdersEquity',
	'ShareholderEquity' : 'StockholdersEquity',
	'StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest' : 'StockholdersEquity'
	}