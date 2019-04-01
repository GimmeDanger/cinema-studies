import requests
import re
import csv
import json
from bs4 import BeautifulSoup

class VarietyParseFormat:
    host_name = "https://variety.com"
    categories = ["news", "reviews", "columns"]
    min_page_num = 1
    max_page_num = 100000 #inf    
    def hay_page_URL(self, cat_name, page_num):
        return f"{self.host_name}/v/film/{cat_name}/page/{page_num}"
    def needle_URL_regexp(self, cat_name):
        return f"^{self.host_name}/\d*/film/{cat_name}"
      
# Finds all urls on <html_page>
# and saves them into <urls_set>,
# url must satisfy <url_regexp> pattern
def gather_page_urls(response, url_regexp, urls_set):
    html_page = response.text
    soup = BeautifulSoup(html_page, "lxml")
    for link in soup.findAll('a', attrs={'href': re.compile(url_regexp)}):
        urls_set.add(link.get('href'))
    return response.status_code
        
def gather_site_pages(min_page_num, max_page_num, categories, needle_URL_regexp, hay_page_URL):
    urls_by_categories = {}
    for cat_name in categories:
        urls = set()
        needle_pattern = needle_URL_regexp(cat_name)
        print("Category", cat_name, "parsing beginned!")
        for page_num in range(min_page_num, max_page_num):
            if page_num % 5 == 0:
              print("Current page: ", page_num)
            hay_url = hay_page_URL(cat_name, page_num)            
            response = requests.get(hay_url)
            status = gather_page_urls(response, needle_pattern, urls)
            if status == 400:
                break
        print("Category", cat_name, "parsing finished!\n")
        urls_by_categories[cat_name] = urls
    return urls_by_categories
  
def dump_parsed_data (output_filename, categories, urls_by_categories, uid_beg):
  f = csv.writer(open(output_filename, "a"))
  f.writerow(["uid", "category", "url"])
  uid = uid_beg
  for cat_name in categories:
    for url in urls_by_categories[cat_name]:
      f.writerow([uid, cat_name, url])
      uid += 1

# Save intermediate results

cat_name = input()

uid = 0
delta_page = 25
variety_format = VarietyParseFormat()

for min_page in range(variety_format.min_page_num, variety_format.max_page_num, delta_page):
  urls = gather_site_pages(min_page_num=min_page,
                           max_page_num=min(variety_format.max_page_num, min_page+delta_page),
                           categories=[cat_name], 
                           needle_URL_regexp=variety_format.needle_URL_regexp,
                           hay_page_URL=variety_format.hay_page_URL)
  dump_parsed_data(output_filename=f"variety_{cat_name}_urls_records.csv",
                   categories=[cat_name],
                   urls_by_categories=urls,
                   uid_beg=uid)
  uid += len(urls[cat_name])
    
