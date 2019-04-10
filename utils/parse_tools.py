import requests
import csv

#for html parsing
from bs4 import BeautifulSoup 
import re

#site pages formats 
from utils import parse_formats
      
# Finds all urls on <html_page>
# and saves them into <urls_set>, url must satisfy <url_regexp> pattern
def gather_page_urls(html_page, url_regexp, urls_set):
    soup = BeautifulSoup(html_page, "lxml")
    for link in soup.findAll('a', attrs={'href': re.compile(url_regexp)}):
        urls_set.add(link.get('href'))
        
# Go through site pages [<min_page_num>, <max_page_num>] in all sections from <categories>
# and look for url <needle_URL_regexp(cat_name)> in <hay_page_URL(cat_name, page_num)>
# Returs set <urls_by_categories>
def gather_site_pages(min_page_num, max_page_num, categories, needle_URL_regexp, hay_page_URL):
    urls_by_categories = {}
    for cat_name in categories:
        urls = set()
        needle_pattern = needle_URL_regexp(cat_name)
        print("Category", cat_name, "parsing beginned!")
        for page_num in range(min_page_num, max_page_num):
            if page_num % 1 == 0:
              print("Current page: ", page_num)
            hay_url = hay_page_URL(cat_name, page_num)            
            response = requests.get(hay_url)
            if response.status_code != 400:
              gather_page_urls(response.text, needle_pattern, urls)
            else:
              break
        print("Category", cat_name, "parsing finished!\n")
        urls_by_categories[cat_name] = urls
    return urls_by_categories
  
def dump_parsed_data_as_csv (output_filename, categories, urls_by_categories, uid_begin):
  f = csv.writer(open(output_filename, "a"))
  f.writerow(["uid", "category", "url"])
  uid = uid_begin
  for cat_name in categories:
    for url in urls_by_categories[cat_name]:
      f.writerow([uid, cat_name, url])
      uid += 1
  return uid    