#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Notebook for experiments in gathering data


# In[15]:


import os
import re
import csv
import requests
import warnings
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm, tqdm_notebook
#warnings.filterwarnings('ignore')


# In[16]:


media_name = 'variety'
df_path = f"../1-most-common-page-structure/mod_df/mod_{media_name}_df.csv"
errors_path = f"../1-most-common-page-structure/errors/{media_name}_errors.csv"


# In[19]:


df = pd.read_csv(df_path)
df = df.drop_duplicates()
err_df = pd.read_csv(errors_path)
err_df = err_df.drop_duplicates()
print("df size =", len(df))
print("err_df size =", len(err_df))
err_df.head()


# In[11]:


try:
    os.mkdir(media_name)
except:
    print("cannot create dir")

#df_article_class_names = ["article__body js-fitvids-content", "longform__body-primary"]
df_meta_names = ['content_type', 'topics', 'title', 'author', 'published_at', 'tags']


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


# In[31]:


#from bs4 import BeautifulSoup
'''
def get_article_text(html_text):
    soup = BeautifulSoup(html_text, "lxml")
    for class_name_str in df_article_class_names:
        mydivs = soup.find("div", {"class": class_name_str})
        if mydivs != None:
            text = ''
            for p in mydivs.find_all("p"):
                text += p.text + ' '
            return text
    return None
'''

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
    return get_article_meta(html_text, df_meta_names)

#get_article_meta_test()


# In[26]:


def parse_article_urls(df, err_df, meta_names):    
    modified_df = df        
    cannot_parsed = {} # {url : reason}
    with tqdm(desc="rows", total=len(err_df)) as pbar_outer:
        for row in err_df.itertuples():
            url = getattr(row, 'url')
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
                df_row = df.loc[df.article_url == url].to_dict()
                index = list(df_row['text_path'].keys())[0]
                text_path = list(df_row['text_path'].values())[0]
                for name in meta_names:
                    if name in article_meta:
                        modified_df.at[index,name] = article_meta[name]        
                file = open(text_path,'w')
                file.write(article_text)  
                file.close()
            except:
                cannot_parsed[url] = 'cannot save data'
            pbar_outer.update(1)
    return (modified_df, cannot_parsed)


# In[27]:


mod_df, errors = parse_article_urls(df, err_df, df_meta_names)


# In[28]:


errors


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


mod_df = mod_df.drop(df.columns[0], axis=1)


# In[13]:


mod_df.to_csv(f"full_{media_name}_df.csv", index=True)


# In[28]:


'''
df = pd.read_csv(f'./full_df/full_hollywood_reporter_df.csv')
err_df = pd.read_csv('hollywood_reporter_errors.csv')
print(len(df), len(err_df))

for row in err_df.itertuples():
    url = getattr(row, 'url')
    df_row = df.loc[df.article_url == url].to_dict()
    index = list(df_row['text_path'].keys())[0]
    df = df.drop(index=index)
len(df)    

print(len(df), len(err_df))

df = df.drop(df.columns[0], axis=1)
df.to_csv(f"full_{media_name}_df.csv", index=True)
'''

