import feedparser
import urllib
from lxml import etree as ET
import re


contents = urllib.request.urlopen("https://www.sec.gov/Archives/edgar/usgaap.rss.xml", )
#contents = urllib.request.urlopen("http://www.sec.gov/Archives/edgar/data/350797/000114420418066592/0001144204-18-066592-index.htm")

#contents = urllib.unquote(contents)

tree = ET.parse(contents)
    # get root elememen 
root = tree.getroot()

for child in root.iter('{http://www.sec.gov/Archives/edgar}xbrlFile'):
	print(child.tag,child.attrib,child.text)

