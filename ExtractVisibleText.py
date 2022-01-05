# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 11:34:37 2021

@author: harres.tariq
"""
from selenium import webdriver
import time
from bs4 import BeautifulSoup, Comment
import re
# %%
class ExtractVisibleText:
    
    _driver=''
    _url=''
    _debug_var=''
    _title=''
    
    def __init__(self, driver_path,url):
        self._url=url
        self._driver=self.make_ChromeWebDriver(driver_path)        

    def delete(self):
        self.close_ChromeWebDriver()
        del self._url
        del self._driver
        
    def make_ChromeWebDriver(self, driver_path):
        options = webdriver.ChromeOptions();
        options.add_argument('headless');
        driver = webdriver.Chrome(driver_path,options=options)
        return driver

    def close_ChromeWebDriver(self):
        self._driver.quit()
        
    def tag_visible(self,element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]','h1','h2','h3','h4','h5','h6','section','form','input']:
            return False
        if isinstance(element, Comment):
            return False
        #matches=['promo','ads','advertisement', 'excerpt','hidden','http', 'headline', 'msg']
        matches=['promo','ads','advertisement', 'excerpt','hidden', 'headline', 'msg', 'meta','nav','btn']
        for m in matches:
            if (m in ''.join(str(x) for x in element.parent.attrs.values())) | (m in ''.join(str(x) for x in element.parent.attrs.keys())):
                return False
        return True
    
    def text_from_html(self,html):
        
        html_new=re.sub(r'<footer.*', '', html, flags=re.DOTALL).strip()
        #html_new=re.sub(r'<header.*', '', html_new, flags=re.DOTALL).strip()
        soup = BeautifulSoup(html_new, 'html.parser')
        
        non_display=soup.find_all(style=re.compile('display: none'))
        for nd in non_display:
            nd.decompose()
            
        non_display=soup.find_all(style=re.compile('display:none'))
        for nd in non_display:
            nd.decompose()
            
        cmnts=soup.find_all("div", class_="comment")
        for c in cmnts:
            c.decompose()
        
        meta=soup.find_all("div", class_=re.compile('meta'))
        for m in meta:
            m.decompose()
            
        time=soup.find_all(class_=re.compile('time'))
        for t in time:
            t.decompose()
            
        footer=soup.find_all(class_=re.compile('footer'))
        for f in footer:
            f.decompose()
            
        border=soup.find_all(class_=re.compile('border'))
        for b in border:
            b.decompose()
            
        elements=soup.find_all(id=re.compile('bar'))
        for e in elements:
            e.decompose()
            
        elements=soup.find_all(class_=re.compile('sidebar'))
        for e in elements:
            e.decompose()
            
        elements=soup.find_all(id=re.compile('header'))
        for e in elements:
            e.decompose()
            
        elements=soup.find_all(href=re.compile('video'))
        for e in elements:
            e.decompose()
        #        
#        elements=soup.find_all(class_=re.compile('video'))
#        for e in elements:
#            e.decompose()
#        self._debug_var=soup.prettify()    
#        elements=soup.find_all(class_=re.compile('wrap'))
#        for e in elements:
#            e.decompose()

        blacklisted=['time','h1','h2','h3', 'header','li','ul','lis','figure','form','button','nav','option']
        elements=soup.find_all(blacklisted)
        for e in elements:
            e.decompose()
        
        texts = soup.find_all(text=True)
        #print(texts)
        
        visible_texts = filter(self.tag_visible, texts)  
        ls=[]
        text_ls=[]
        drop_ls=['cookies', 'terms of service', 'more information about', 'revised privacy policy','subscribe']
        for t in visible_texts:
            if t.lower() in drop_ls:
                continue
            else:
                ls.append(len(t.strip()))
                text_ls.append(t.strip())
            
        required_texts=u" ".join(t for t in text_ls if t.count(' ')>=0)
        
        punctuations = '''()-[]{}'"\<>/@#$%^&*_~'''
        no_punct = ""
        for char in required_texts:
           if char not in punctuations:
               no_punct = no_punct + char 
        required_texts=no_punct
        required_texts=re.compile(r'\.{3,}').sub(' ', required_texts)
        
        self._title=soup.find_all('title')[0].find(text=True)
        #print(self._title)        
        
        return required_texts
        #return self._debug_var
    
    def get_visible_text(self):
        try:
            self._driver.get(self._url)
        except Exception as e:
            print('driver exception: ',e)
            time.sleep(5)
        time.sleep(0.9)    
        
        return self.text_from_html(self._driver.page_source)
    
    def get_title(self):
        return self._title
# %%
#dpath=r'C:\Users\harres.tariq\Downloads\selenium_final/chromedriver'
#link='https://www.juvefc.com/cristiano-ronaldo-we-can-do-it-together/'
#evt=ExtractVisibleText(dpath,link)
#txt=evt.get_visible_text()
#title=evt.get_title()
#evt.delete()
#print(txt)
