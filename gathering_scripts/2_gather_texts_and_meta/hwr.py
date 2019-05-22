#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Notebook for experiments in gathering data


# In[2]:


import os
import re
import csv
import requests
import warnings
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm, tqdm_notebook
warnings.filterwarnings('ignore')


# In[3]:


df_path = '../../raw_data/film_media_df.csv'


# In[4]:


df = pd.read_csv(df_path)
#df.head()


# In[5]:


os.mkdir("hollywood_reporter")
hwr_article_class_name = "article__body js-fitvids-content"
hwr_meta_names = ['title', 'description', 'date', 'author', 'vertical', 'tags']
hwr_df = df.loc[df.media == "hollywood_reporter"]
#hwr_df.head()


# In[6]:


# import requests
def get_html(url):
    fake_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers=fake_headers)
    return response.text

def get_html_test():
    hwr_test_url = 'https://www.hollywoodreporter.com/news/elle-fanning-uma-thurman-diane-kruger-hit-pradas-resort-2020-show-1207308'
    return get_html(hwr_test_url)

#print(get_html_test())


# In[7]:


#from bs4 import BeautifulSoup
def get_article_text(html_text, class_name_str):
    soup = BeautifulSoup(html_text, "lxml")
    mydivs = soup.find("div", {"class": class_name_str})
    text = ''
    for p in mydivs.find_all("p"):
        text += p.text + ' '
    return text

def get_article_meta(html_text, meta_names):
    ret = {}
    soup = BeautifulSoup(html_text, "lxml")
    for name in meta_names:        
        ret[name] = soup.find("meta", {"name": "sailthru."+name})['content']
    return ret

def get_article_text_test():    
    hwr_test_url = 'https://www.hollywoodreporter.com/news/elle-fanning-uma-thurman-diane-kruger-hit-pradas-resort-2020-show-1207308'
    hwr_html_text = get_html(hwr_test_url)
    return get_article_text(hwr_html_text, hwr_article_class_name)

def get_article_meta_test():    
    hwr_test_url = 'https://www.hollywoodreporter.com/news/elle-fanning-uma-thurman-diane-kruger-hit-pradas-resort-2020-show-1207308'
    hwr_html_text = get_html(hwr_test_url)
    return get_article_meta(hwr_html_text, ['title', 'description', 'date', 'author', 'vertical', 'tags'])

#get_article_meta_test()


# In[8]:


def parse_article_urls(df):    
    modified_df = df
    # expand dataframe, add columns for meta
    for meta_name in hwr_meta_names:
        modified_df[meta_name] = None
        
    cannot_parsed = {} # {url : reason}
    with tqdm(desc="rows", total=len(df)) as pbar_outer:
        for row in df.itertuples():
            url = getattr(row, 'article_url')
            # part 0: get html text
            html_text = None
            try:
                html_text = get_html(url)
            except:
                cannot_parsed[url] = 'cannot get html'
                pbar_outer.update(1)
                continue                
            # part 1: get article text
            article_text = None
            try:
                article_text = get_article_text(html_text, hwr_article_class_name)                          
            except:
                cannot_parsed[url] = 'cannot get text'
                pbar_outer.update(1)
                continue
            # part 2: get article meta
            article_meta = None
            try:
                article_meta = get_article_meta(html_text, hwr_meta_names)
            except:
                cannot_parsed[url] = 'cannot get meta'
                pbar_outer.update(1)
                continue
            # part 3: save data
            try:
                for meta_name in hwr_meta_names:
                    modified_df.at[getattr(row,'Index'),meta_name] = article_meta[meta_name]
                file = open(getattr(row,'text_path'),'w')
                file.write(article_text)  
                file.close()
            except:
                cannot_parsed[url] = 'cannot save data'
            pbar_outer.update(1)
    return (modified_df, cannot_parsed)


# In[9]:


mod_hwr_df, errors = parse_article_urls(hwr_df)


# In[10]:


if len(errors)>0:
    file = open(f'hwr_errors.csv', "w")
    f = csv.writer(file)
    f.writerow(["url", "reason"])
    for key, value in errors.items():
      f.writerow([key, value])
    file.close()
    
mod_hwr_df.head()


# In[11]:


#mod_hwr_df.head()


# In[12]:


mod_hwr_df.to_csv("mod_hwr_df.csv", index=True)


# In[ ]:




