import datetime
import lxml.html as parser
import requests
import csv
import pandas as pd
from bs4 import BeautifulSoup
import json


############################################################

Dados_TrabalhaBrasil = []



for i in range(1, 251):
    
    url_api = "https://www.trabalhabrasil.com.br/api/v1.0/Job/List?idFuncao=0&idCidade=0&pagina={numero_da_pagina}&pesquisa=vagas&ordenacao=1&idUsuario=".format(numero_da_pagina = i)
    print(url_api)
############################################################   

    r = requests.get(url_api)
    r.status_code
    soup = BeautifulSoup(r.text)
    
    url_json_text = json.loads(r.text)
############################################################    
# SCRAP DOS CODIGOS E LINKS

    #ados_TrabalhaBrasil = []
    
    for elemento in url_json_text: 
        
        try:
            codigo = elemento['id']
        except:
            codigo = "-"
               
            
        url = elemento['u']
        links = "https://www.trabalhabrasil.com.br/" + url  
        try:
            links = "https://www.trabalhabrasil.com.br/" + url
        except:
            links = "-"
        
        
        try:
            nome_vaga = elemento['df']
        except: 
            nome_vaga = "-"
            
     
        try:
            salario = elemento['sl']
        except: 
            salario = "-"
            
    
        try:
            vagas = elemento['qv']
        except: 
            vagas = "-"
                          
                
        try:
            local = elemento['dc'] + ' - ' + elemento['uf']
        except: 
            local = "-"

            
        try:
            dados_da_empresa = elemento['ne']
        except: 
            dados_da_empresa = "-"

            
        try:
            pcd = elemento['pcd'] #elemento['pcd'] = none
        except: 
            pcd = "-"
    
    
        url_dos_links = links
        
        req = requests.get(url_dos_links).text # content (would be preferred for "binary" filetypes, such as an image or PDF file)
        
        soup = BeautifulSoup(req, 'html.parser')
        
             
        try:
            data = soup.find('div',{'class':"col-md-3 remove__padding text-center"}).p.getText()

        except:
            data = "-"
        
        
        try:
            regime = soup.findAll('dd',{'class':"job-plain-text"})[-1].getText().replace('\r','').replace('\n','').replace('    ','').replace('do','do ')

        except:    
            regime = "-"
     
        
        try:
            descricao = soup.find('p',{'class':"job-plain-text"}).getText().replace('\r','').replace('\n','').replace('  ','')

        except:
            descricao = "-"
        


        data_scraping = datetime.datetime.now().strftime('%d/%m/%Y')

        
        try:
            data_expiracao = soup.findAll('div',{'class':"flex-row flex-wrap justify-center"})[-1].getText().replace('\n','')
        except:
            data_expiracao = str('-')
        
        
        dados = {
                'Url':links,
                'Código':codigo,
                'Nome_Vaga':nome_vaga,
                "Salário":salario ,
                "Vagas":vagas,
                "Localidade":local,
                "Data":data,
                "Data de expiração":data_expiracao,
                "Conteúdo":descricao,
                #"Benefícios":
                #'Horário':
                'Regime':regime,
                #'Adicional':
                'Dados da Empresa':dados_da_empresa,
                'Pcd':pcd,
                "Data do scraping":data_scraping}
             
        
        Dados_TrabalhaBrasil.append(dados)  
        
        
        #print('Scraping....')
        
#   TrabalhaBrasil = pd.DataFrame(Dados_TrabalhaBrasil) 
#   TrabalhaBrasil = TrabalhaBrasil.fill()
#   df = TrabalhaBrasil.stack()
#   df =  df.reset_index()
#   df = df.rename(columns={'level_0': 'ID','level_1':'TAG',0:'TEXTO'}, inplace=True)
#   df.to_csv('file.csv', index=False)
      


df = pd.DataFrame(Dados_TrabalhaBrasil)
df.to_csv('Dados_TrabalhaBrasil2.csv')