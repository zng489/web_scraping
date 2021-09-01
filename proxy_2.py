import sys
import pandas as pd
import numpy as np
import requests
import time
import urllib3
import itertools
import time
from bs4 import BeautifulSoup
from requests.api import head


from random import randint
from time import sleep


import requests
from lxml.html import fromstring

from lxml.html import fromstring
import requests
from itertools import cycle
import traceback

def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:20]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            #Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies

def t0():
    proxies = get_proxies()
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}
    df = pd.read_csv('Vagas_v1_t0.csv')
    df_c = df['Código'].tolist()
    df_u = df['Url'].tolist()
    connected = []
    error = []

    proxy_pool = cycle(proxies)
    url = 'https://httpbin.org/ip'
    for i in range(1,21):
        proxy = next(proxy_pool)
        print("Request #%d"%i)
        try:

            for (i,q) in zip(df_u,df_c):
                r = requests.get(i,proxies={"http": proxy, "https": proxy},allow_redirects=False, headers=headers, timeout=10).text
                req = requests.get(i,allow_redirects=False)
                soup = BeautifulSoup(r, 'lxml')

                try:
                    if soup.find_all('div',{'class':'job-expired__text'}) == False: #or req.status_code == 200:
                        print(req.status_code)
                        print(i,q,"A vaga permanece (Connected)")
                        urls = i
                        cods = q
                        dados = {'urls':urls,'cods':cods}
                        print(len(urls))
                        connected.append(dados)
                        df_0 = pd.DataFrame(connected)
                        print(df_0.count())
                        df_0.to_csv('Vagas_existentes.csv')
                        sleep(randint(0,10))

                    else:

                        print(i,q,'Não há mais essa vaga (Error)')
                        urls = i
                        cods = q
                        dados = {'urls':urls,'cods':cods}
                        print(len(urls))
                        error.append(dados)
                        df_1 = pd.DataFrame(error)
                        df_1.to_csv('Vagas_excluidas.csv')
                        sleep(randint(0,10))
                except:
                    print(sys.exc_info())

            #print(response.json())
        except:
            print("Skipping. Connnection error")


    return print(error)

if __name__ == '__main__':
    t0()