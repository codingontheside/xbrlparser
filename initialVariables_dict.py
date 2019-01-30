financials_list = {\
'Profit' : ['GrossProfit','NetIncomeLoss'],\
'EarningsPerShare' : ['EarningsPerShareBasic','EarningsPerShareBasicAndDiluted'],\
'CurrentAssets' : ['AssetsCurrent', 'Assets'],\
'CurrentLiabilities' : ['LiabilitiesCurrent','LongTermDebtCurrent','Liabilities'],\
'DividendsPaid' : ['CommonStockDividendsPerShareDeclared','CommonStockDividendsPerShareCashPaid'],\
'SharesOutstanding' : ['CommonStockSharesOutstanding', 'WeightedAverageNumberOfSharesOutstandingBasic','SharesOutstanding'],\
'Stockholders Equity' : ['StockholdersEquity', 'ShareholderEquity','StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest']\
}

screenerValues = {\
'Growth Rate' : ['>=',110.0],\
'Growth Periods' : ['>=',2],\
'Current Ratio' : ['>=',2.0],\
'Dividend Record' : ['==',False],\
'PE Ratio' : ['<=',45.0],\
'Market Value' : ['>=',100000000.0],\
'Price to Book' : ['<=',12.5]\
}