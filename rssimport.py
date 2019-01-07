import feedparser
import urllib
from lxml import etree as ET
import re


contents = urllib.request.urlopen("https://www.sec.gov/Archives/edgar/usgaap.rss.xml", )

tree = ET.parse(contents)
    # get root elememen 
root = tree.getroot()

URLset = []

for child in root.iter('{http://www.sec.gov/Archives/edgar}xbrlFile'):
	description = child.attrib.get('{http://www.sec.gov/Archives/edgar}description')
	if description == 'XBRL INSTANCE DOCUMENT':
		for child2 in child.iter('*'):
			XBRL_URL = child2.attrib.get('{http://www.sec.gov/Archives/edgar}url')
			URLset.append(XBRL_URL)
		#print(child.attrib)
	else:
		continue

return URLset;
