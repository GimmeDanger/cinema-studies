import re
import requests
from utils import parse_tools 
from utils import parse_formats

site_format = parse_formats.HWReporterParseFormat("female%20directors")

#https://www.hollywoodreporter.com/search/women%20director?page=1&filters=type:news%20tid:59
#https://www.hollywoodreporter.com/search/women%20director?page=1&filters=type:review%20tid:59

fake_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
#hay_url = 'https://www.hollywoodreporter.com/search/female%20directors?page=100&filters=type%3Anews+tid%3A59'
hay_url = site_format.hay_page_URL("news", 100)
response = requests.get(hay_url, headers=fake_headers)
#print(response.text)

urls = set()
needle_pattern = site_format.needle_URL_regexp()
parse_tools.gather_page_urls(response.text, needle_pattern, urls)         
print(len(urls))
print(urls)
