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
import datetime
import time
import csv

from bs4 import BeautifulSoup
import requests
import csv


import aiohttp
import asyncio

#!pip install nest-asyncio
import nest_asyncio
#nest_asyncio.apply()


async def main():
    dados_infojobs = []
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
          
    async with aiohttp.ClientSession(headers=headers) as session:
        
        df = pd.read_csv('Infojobs_t0_consolidada_asct.csv',index_col=0)
        df_list_url = df['url'].to_list()
        
        for link in df_list_url:
        
            cada_link = link
            async with session.get(link) as response:
                print("Status:", response.status)
                print("Content-type:", response.headers['content-type'])

            
                html = await response.text()
                print("Body:", html[:15], "...")
                
                
                try:
                    soup = BeautifulSoup(html, "html.parser")
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
                        'url':link}
                    dados_infojobs.append(dados)
                    df = pd.DataFrame(dados_infojobs)
                    df.to_csv('dados_infojobs_teste.csv')
                    
                except:
                    print('url nao existe mais')

asyncio.run(main())            