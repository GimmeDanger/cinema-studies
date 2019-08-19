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
media_name = 'deadline'


# In[4]:


df = pd.read_csv(df_path)
print(len(df))
print(df['media'].unique())
#df.head()


# In[5]:


df = df.loc[df.media == media_name]
print(len(df))
#df.head()


# In[6]:


# import requests
def get_html(url):
    fake_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers=fake_headers)
    return response.text

def get_html_test():
    test_url = df.iloc[0]['article_url']
    print(test_url)
    print(get_html(test_url))

#get_html_test()


# In[7]:


#from bs4 import BeautifulSoup
def get_article_text(html_text):
    soup = BeautifulSoup(html_text, "lxml")
    text = soup.find("meta", {"name": 'body'})['content']
    return text

def get_article_meta(html_text, meta_names):
    ret = {}
    soup = BeautifulSoup(html_text, "lxml")
    for name in meta_names:
        for meta in soup.find_all("meta", {"name": name}):
            if name not in ret:
                ret[name] = meta['content']
            elif ret[name] != meta['content']:
                ret[name] = ret[name] + ', ' + meta['content']
    return ret

def get_article_text_test():    
    test_url = df.iloc[0]['article_url']
    html_text = get_html(test_url)
    return get_article_text(html_text)

def get_article_meta_test():    
    test_url = df.iloc[0]['article_url']
    html_text = get_html(test_url)
    return get_article_meta(html_text, ['content_type', 'topics', 'title', 'author', 'published_at', 'tags'])

#get_article_meta_test()


# In[8]:


try:
    os.mkdir(media_name)
except:
    print("cannot create dir")
    
df_meta_names = ['content_type', 'topics', 'title', 'author', 'published_at', 'tags']


# In[9]:


def parse_article_urls(df, meta_names):    
    modified_df = df
    # expand dataframe, add columns for meta    
    for name in meta_names:
        modified_df[name] = None
        
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
                article_text = get_article_text(html_text)                          
            except:
                cannot_parsed[url] = 'cannot get text'
                pbar_outer.update(1)
                continue
            # part 2: get article meta
            article_meta = None
            try:
                article_meta = get_article_meta(html_text, meta_names)
            except:
                cannot_parsed[url] = 'cannot get meta'
                pbar_outer.update(1)
                continue
            # part 3: save data
            try:                
                for name in meta_names:
                    modified_df.at[getattr(row,'Index'),name] = article_meta[name]
                file = open(getattr(row,'text_path'),'w')
                file.write(article_text)  
                file.close()
            except:
                cannot_parsed[url] = 'cannot save data'
            pbar_outer.update(1)
    return (modified_df, cannot_parsed)


# In[10]:


mod_df, errors = parse_article_urls(df, df_meta_names)


# In[11]:


if len(errors)>0:
    file = open(f'{media_name}_errors.csv', "w")
    f = csv.writer(file)
    f.writerow(["url", "reason"])
    for key, value in errors.items():
      f.writerow([key, value])
    file.close()
    
#mod_df.head()    


# In[12]:


mod_df.to_csv("mod_df.csv", index=True)

