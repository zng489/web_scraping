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

sleep(randint(0,10))


def t0():

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}
    df = pd.read_csv('Vagas_v1_t0.csv')
    df_c = df['Código'].tolist()
    df_u = df['Url'].tolist()
    connected = []
    error = []

    for (i,q) in zip(df_u,df_c):
        #proxies = {'https': "socks5h://127.0.0.1:1080"}
        # #r = requests.get(i,proxies=proxies)
        #r = requests.get(i, timeout=600)  
        #proxies = {"http":'http://165.22.64.68:40402',"http":'http://43.224.10.42:6666'}
        #r = requests.get(i, proxies=proxies)

        r = requests.get(i, allow_redirects=False, headers=headers, timeout=200,verify=False).text
        req = requests.get(i,allow_redirects=False,verify=False)
        soup = BeautifulSoup(r, 'lxml')
        #if r.status_code == 200:

        
        try:
            if soup.find_all('div',{'class':'job-expired__text'}) == [] and soup.find_all('h2',{'class':'tit-nao-encontrado titulo'}) == []: #or req.status_code == 200:
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

    #    http = urllib3.PoolManager()
    #    r = http.request('GET',i,retries=urllib3.Retry(redirect=2, raise_on_redirect=False))
#
    #    if r.status == 200:
    #        time.sleep(2)
    #        print(i,q,"Connected")
    #        urls = i
    #        cods = q
    #        dados = {'urls':urls,'cods':cods}
    #        connected.append(dados)
    #        df_0 = pd.DataFrame(connected)
    #        print(df_0.count())
    #        df_0.to_csv('connected.csv')

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


                #time.sleep(2)

        except:
            print(sys.exc_info())
            
    return print(error)

if __name__ == '__main__':
    t0()