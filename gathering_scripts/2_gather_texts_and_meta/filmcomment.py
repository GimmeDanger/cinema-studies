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
media_name = 'filmcomment'


# In[9]:


df = pd.read_csv(df_path)
print(len(df))
print(df['media'].unique())
df.head()


# In[10]:


df = df.loc[df.media == media_name]
print(len(df))
df.head()


# In[32]:


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


# In[34]:


#from bs4 import BeautifulSoup
def get_article_text(html_text):
    soup = BeautifulSoup(html_text, "lxml")
    mydivs = soup.find("div", {"class": 'post-content'})
    text = ''
    for p in mydivs.find_all("p"):
        text += p.text + ' '
    return text

def get_article_meta(html_text, meta_names):
    ret = {}
    soup = BeautifulSoup(html_text, "lxml")
    for name in meta_names:
        for meta in soup.find_all("meta", {"property": name}):
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
    return get_article_meta(html_text, ['og:type', 'og:title', 'og:description', 'article:section', 'article:published_time'])

#get_article_meta_test()


# In[35]:


try:
    os.mkdir(media_name)
except:
    print("cannot create dir")
    
df_meta_names = ['og:type', 'og:title', 'og:description', 'article:section', 'article:published_time']


# In[39]:


def parse_article_urls(df, meta_names):    
    modified_df = df
    # expand dataframe, add columns for meta    
    for name in meta_names:
        prefix, real_name = name.split(':')
        modified_df[real_name] = None
        
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
                print(article_meta)
            except:
                cannot_parsed[url] = 'cannot get meta'
                pbar_outer.update(1)
                continue
            # part 3: save data
            try:
                for name in meta_names:
                    prefix, real_name = name.split(':')
                    if name in article_meta:
                        modified_df.at[getattr(row,'Index'),real_name] = article_meta[name]    
                file = open(getattr(row,'text_path'),'w')
                file.write(article_text)  
                file.close()
            except:
                cannot_parsed[url] = 'cannot save data'
            pbar_outer.update(1)
    return (modified_df, cannot_parsed)


# In[40]:


mod_df, errors = parse_article_urls(df, df_meta_names)


# In[42]:


#errors


# In[43]:


if len(errors)>0:
    file = open(f'{media_name}_errors.csv', "w")
    f = csv.writer(file)
    f.writerow(["url", "reason"])
    for key, value in errors.items():
      f.writerow([key, value])
    file.close()
    
#mod_df.head()    


# In[44]:


mod_df.to_csv(f"mod_{media_name}_df.csv", index=True)


# In[ ]:




