# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 12:05:07 2021

@author: harres.tariq
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 11:33:24 2021

@author: harres.tariq
"""
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import urllib
# %%
class GoogleImageDownload:
    
    _search_phrase=''
    _driver=''
    _debug_var=''
    _srcs=[]
    _ipath=''
    
    def __init__(self, search_phrase, driver_path,image_path):
        self._search_phrase=search_phrase
        self._driver=self.make_ChromeWebDriver(driver_path)
        self._ipath=image_path
        self._run()

    def delete(self):
        self.close_ChromeWebDriver()
        del self._search_phrase
        del self._driver
        del self._srcs
        del self._ipath
    
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
        url = "https://www.google.com/search?gl=us&tbm=isch&q="+query
        try:
            self._driver.get(url)
        except Exception as e:
            print('driver exception: ',e)
            time.sleep(5)
        time.sleep(0.9)
        
    def get_image_links(self):
        soup = BeautifulSoup(self._driver.page_source,'html.parser')
        imgs=soup.find_all(class_='rg_i Q4LuWd', src=True)
        #self._debug_var=cards
        srcs=[]
        for i in imgs:
            srcs.append(i.attrs['src'])
            
        self._srcs=srcs
    
    def _run(self):
        self.search_google()
        self.get_image_links()
        
    def download_nth_image(self,n):
        urllib.request.urlretrieve(self._srcs[n],self._ipath+'\\'+self._search_phrase+str(n)+'.png')
        
    def download_top_n_images(self,n):
        for i in range(n):
            urllib.request.urlretrieve(self._srcs[i],self._ipath+'\\'+self._search_phrase+str(i)+'.png')
        
# %%
dpath=r'C:\Users\harres.tariq\Downloads\selenium_final/chromedriver'
ipath=r'E:\work related\huggingface\python_code\images'
# %%
search_phrase='neymar injury'
gid=GoogleImageDownload(search_phrase,dpath,ipath)
gid.download_top_n_images(5)
#gid.delete()
#print(topstories)