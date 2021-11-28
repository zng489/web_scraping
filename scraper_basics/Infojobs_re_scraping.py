from lxml import html
import requests
import bs4
import json
import pandas as pd
import numpy as np
import csv
from random import randint
from datetime import date
from time import sleep

from selenium import webdriver   # for webdriver
from selenium.webdriver.support.ui import WebDriverWait  # for implicit and explict waits
from selenium.webdriver.chrome.options import Options  # for suppressing the browse
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import datetime
import time
import csv

from bs4 import BeautifulSoup
import requests
import csv


class Infojobs():

    #headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
    #df = pd.read_csv('Infojobs_t0_consolidada_asct.csv',index_col=0)
    #list = df['url'].to_list()
    
    def __init__(self,list_url):
        self.baseurl = list_url

        for every_url in list_url:
            #print(every_url)
            cada_link = every_url

        return None #or __init__() should return None, not 'str'
        
    def url_chosen(cada_link):
        dados_infojobs = []

        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
          
        try:
            re = requests.get(cada_link,allow_redirects=False, headers=headers,timeout=200).text
            soup = BeautifulSoup(re, "html.parser")
            time.sleep(2)    
            r = requests.get(cada_link,allow_redirects=False)
        except:
            re = requests.get(cada_link,allow_redirects=False, headers=headers,timeout=200).text
            soup = BeautifulSoup(re, "html.parser")
            time.sleep(2)
            r = requests.get(cada_link,allow_redirects=False)
                             
        if r.status_code == 200:
            url = cada_link
            
            try:
                #len(soup.findAll('ol',{'class':'descriptionItems'})) ==> 3                    
                conteudo = soup.findAll('ol',{'class':'descriptionItems'})[0].getText().strip().replace('\r','').replace('\n','').strip()                  
            except:
                conteudo = 'None'
                    
            try:   
                exigencias = soup.findAll('ol',{'class':'descriptionItems'})[1].getText().strip().replace('\r','').replace('\n','').strip()
            except:
                exigencias = 'None'
                
            try:
                beneficios = soup.findAll('ol',{'class':'descriptionItems'})[2].getText().strip().replace('\r','').replace('\n','').strip()
            except:
                beneficios = 'None'

                
            dados = {'conteudo':conteudo,
                    'exigencias':exigencias,
                    'beneficios':beneficios,
                    'url':url}
            
            dados_infojobs.append(dados)
            
            df = pd.DataFrame(dados_infojobs)
            df.to_csv('dados_infojobs.csv')

        else:
            print('url nao existe mais')
            
        return cada_link
                             
def main():
    df = pd.read_csv('Infojobs_t0_consolidada_asct.csv',index_col=0)
    df_list_url = df['url'].to_list()
    Infojobs(df_list_url) # list_url = df_list_url
                             
if __name__ == "__main__":
    main()