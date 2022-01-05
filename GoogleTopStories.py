# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 11:33:24 2021

@author: harres.tariq
"""
from selenium import webdriver
import time
from bs4 import BeautifulSoup
# %%
class GoogleTopStories:
    
    _search_phrase=''
    _driver=''
    _debug_var=''
    
    def __init__(self, search_phrase, driver_path):
        self._search_phrase=search_phrase
        self._driver=self.make_ChromeWebDriver(driver_path)

    def delete(self):
        self.close_ChromeWebDriver()
        del self._search_phrase
        del self._driver
    
    def make_ChromeWebDriver(self, driver_path):
        options = webdriver.ChromeOptions();
        options.add_argument('headless');
        driver = webdriver.Chrome(driver_path,options=options)
        return driver
    
    def close_ChromeWebDriver(self):
        self._driver.quit()
        
    def search_google(self):
        query=self._search_phrase
        query=query.replace(' ','+')
        url = "https://www.google.com/search?gl=us&q="+query
        try:
            self._driver.get(url)
        except Exception as e:
            print('driver exception: ',e)
            time.sleep(5)
        time.sleep(0.9)
        
    def make_topstories_google_link(self):
        soup = BeautifulSoup(self._driver.page_source,'html.parser')
        view_all_obj=soup.find_all('g-more-link')
        for m in view_all_obj:
            if "More news" in str(m):
                req=m
                #print('found')
                break
        link='https://www.google.com'+req.find(href=True)['href']
        return link
    
    def run_topstories_google_link(self, link):
        try:
            self._driver.get(link)
        except Exception as e:
            print('driver exception: ',e)
            time.sleep(5)
        time.sleep(0.9)
        
    def get_article_links(self):
        soup = BeautifulSoup(self._driver.page_source,'html.parser')
        cards=soup.find_all('g-card')
        self._debug_var=cards
        articles=[]
        times=[]
        for c in cards:
            u=c.find(href=True)['href']
            articles.append(u)
            texts=c.find_all(text=True)
            t=[x for x in texts if 'ago' in x][-1]
            if('min' in t):
                t=int(t.split()[0])/60
            elif('hour' in t):
                t=int(t.split()[0])
            elif('day' in t):
                t=int(t.split()[0])*24
            elif('week' in t):
                t=int(t.split()[0])*7*24
            elif('month' in t):
                t=int(t.split()[0])*30*24
            times.append(t)
            
        return dict(zip(articles, times))
        #return dict(sorted(d.items(), key=lambda item: item[1]))
    
    def get_topstories(self):
        self.search_google()
        topstories_google_link=self.make_topstories_google_link()
        self.run_topstories_google_link(topstories_google_link)
        return self.get_article_links()
# %%
#dpath=r'C:\Users\harres.tariq\Downloads\selenium_final/chromedriver'
#search_phrase='messi'
#gts=GoogleTopStories(search_phrase,dpath)
#topstories=gts.get_topstories()
#gts.delete()
#print(topstories)