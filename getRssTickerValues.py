from daoRefactor2 import DAO
from rssTickerInfo import rssTickerInfo
import json
import boto3

table = 'CompanyRSSFeed'
dao = DAO(table)

def main():
	tickerValues = dao.getRssTickerValues('UNP')
	print(tickerValues)

if __name__ == "__main__": 
  
    # calling main function 
	    main()		
