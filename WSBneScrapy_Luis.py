import sys
import time
import requests
from datetime import datetime
from multiprocessing import Pool
import pandas as pd
from random import randint
from time import sleep
import re
import lxml.html as parser



def definirDataframe(colunas):
    df = pd.DataFrame(columns=colunas)
    return df

def exportarCsv(df, nome):
    df.to_csv(nome, sep=';', encoding="utf-8-sig")

def adicionarConteudoPorLinhaNoDataframe(df, lista):
    df.loc[len(df)] = lista

def obterScrapy(r, xpath):
    try:
        product_html = parser.fromstring(r.text)
        name = product_html.xpath(xpath)
        return name
        #root = html.fragment_fromstring('<p>Hello<br>world!</p>')
        #html.tostring(root, method='text')

    except:
        html_content_vaga = '-'
        return html_content_vaga

def contarqtsvagasexistemnapaginaScrapy(r,xpath):
    product_html = parser.fromstring(r.text)
    name = product_html.xpath(xpath)
    return len(name)

def receberQtdDeVagasQueExistemNaPaginaVagaCertaScrapy(r):
    return contarqtsvagasexistemnapaginaScrapy(r,"//div[@class='mb-8']//h3/a")

def ElementosnapaginaScrapy(r,xpath):
    product_html = parser.fromstring(r.text)
    return product_html.xpath(xpath)

def receberlistaDeVagasQueExistemNaPaginaVagaCertaScrapy(r):
    return ElementosnapaginaScrapy(r,"//h3[text()='Atribuições'or text()='Descrição Geral']//following-sibling::p[@class='job__description__value'][1]/a[text()='Continuar lendo' ]/@href")



def obterConteudoScrapyVaga(r):
    return obterScrapy(r,"//div[@class='job__details__information']//span//following-sibling::strong/text()")


def obterConteudoScrapySalario(r):
    return obterScrapy(r,"//div[@class='job__details__information']//span[text() = 'Salário:']/../text()")


def obterConteudoScrapyQtdVagas():
    return '-'

def obterConteudoScrapyLocalidade(r):
    return obterScrapy(r, "//div[@class='job__details__information']//span[text() = 'Localização:']/../text()")

def obterConteudoScrapyData(r):
    return obterScrapy(r, "//div[@class='job']//h4//span[text() = 'Publicada há:']/../span[@id = 'tag-releaseDate']/text()")

def obterConteudoScrapyContent(r):
    return obterScrapy(r, "//h4[@class='job__description__key' and text()='Atribuições']//following-sibling::h5[1]/text()")

def obterConteudoScrapyBeneficio(r):
    return obterScrapy(r, "//h4[@class='job__description__key' and text()='Benefícios']//following-sibling::h5[1]/text()")

def obterConteudoScrapyHorario():
    return '-'

def obterConteudoScrapyRegime(r):
    return obterScrapy(r, "//h4[@class='job__description__key' and text()='Tipo de Vínculo']//following-sibling::h5[1]/text()")

def obterConteudoScrapyAdicional():
    return '-'


def obterConteudoScrapyDados(r):
    return obterScrapy(r, "//h4[@class='job__description__key' and text()='Descrição Geral']//following-sibling::h5[1]/text()")

def obterCodVagaScrapy(r):
    return obterScrapy(r, "//div[@class='job']//span[text() = 'Código da vaga:']/../text()")


def retornarUrl():
    return "https://www.bne.com.br/"

def obterConteudoDaPaginaScrapy(df,r,url):
        lista = []

        lista.append(url)
        aa = obterCodVagaScrapy(r)
        lista.append(aa)
        a = obterConteudoScrapyVaga(r)
        lista.append(a)
        b = obterConteudoScrapySalario(r)
        lista.append(b)
        bb = obterConteudoScrapyQtdVagas()
        lista.append(bb)
        bbb = obterConteudoScrapyLocalidade(r)
        lista.append(bbb)
        c = obterConteudoScrapyData(r)
        lista.append(c)
        d = obterConteudoScrapyContent(r)
        lista.append(d)
        e = obterConteudoScrapyBeneficio(r)
        lista.append(e)
        f = obterConteudoScrapyHorario()
        lista.append(f)
        g = obterConteudoScrapyRegime(r)
        lista.append(g)
        h = obterConteudoScrapyAdicional()
        lista.append(h)
        i = obterConteudoScrapyDados(r)
        lista.append(i)

        adicionarConteudoPorLinhaNoDataframe(df, lista)
        return df


def receberlistaDeVagasQueExistemNaPaginaBneScrapy(r):
    return ElementosnapaginaScrapy(r, "//h3[text()='Atribuições'or text()='Descrição Geral']//following-sibling::p[@class='job__description__value'][1]/a[text()='Continuar lendo' ]/@href")


def executar(df,listaLinks,init,fim):
    count =0
    for i in range(init, fim):
        print(i)
        links = []
        # BnePage.conectar_VagaCerta(i)
        r = requests.get('https://vagascertas.com.br/vagas?vaga=&estado=&cidade=&area=&pag=%s' % i)
        # links = BnePage.receberQtdDeVagasQueExistemNaPaginaVagaCertaScrapy(r)
        # print(links)
        links = receberlistaDeVagasQueExistemNaPaginaVagaCertaScrapy(r)
        #sleep(randint(0, 2))

        for el in range(len(links)):
            listaLinks.append(links[el])

        '''
        if i == 300 or i == 600 or i == 900 or i == 1200 or i == 1500 or i == 1800:
            time.sleep(20)
            continue
        if i == 150 or i == 450 or i == 750 or i == 1050 or i == 1300 or i == 1650:
            time.sleep(5)
            continue
        '''
    # Acessar links e obter conteudo
    for il in listaLinks:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
            "Accept-Encoding": "*",
            "Connection": "keep-alive"
        }
        r = requests.get(il, headers= headers)
        df = obterConteudoDaPaginaScrapy(df, r, il)
        sleep(randint(0, 2))

        '''
        count = count +1
        if count == 3000 or count == 6000 or count == 9000 or count == 12000 or count == 15000 or count == 16500:
            time.sleep(5000)
            continue
        if count == 1500 or count == 4500 or count == 10050 or count == 13050 or count == 17000 or count == 16500:
            time.sleep(2000)
            continue
        '''
    return df

def multi_run_wrapper(args):
    return executar(*args)

def core(df, listaLinks, init1, fim1, init2, fim2, init3, fim3, init4, fim4):
    df = pool.map(multi_run_wrapper,
                  [(df, listaLinks, init1, fim1), (df, listaLinks, init2, fim2), (df, listaLinks, init3, fim3),
                   (df, listaLinks, init4, fim4)])
    df = pd.concat(df)
    today = datetime.now()
    data = today.strftime('%Y-%m-%d-%H-%M')

    # exportar em csv
    nome_xls = 'vagasCertas' + data + '.csv'
    exportarCsv(df, nome_xls)
    del df

def divPaginas(init1, paginas):
    fim1 = init1 + ((paginas - init1)/4)
    init2 = init1 + round((paginas - init1) / 4)
    fim2 = init1 + round((paginas - init1) / 2)
    init3 = init1 + round((paginas - init1) / 2)
    fim3 = init1 + round((paginas - init1) / 2) + round((paginas - init1) / 4)
    init4 = init1 + round((paginas - init1) / 2) + round((paginas - init1) / 4)
    fim4 = 1 + round(init1 + ((paginas - init1) / 2) + ((paginas - init1) / 4) + ((paginas - init1) / 4))
    return int(init1),int(fim1),int(init2), int(fim2),int(init3),int(fim3),int(init4),int(fim4)


if __name__ == '__main__':
    class BneExecutor:
        pass

    try:
        pool = Pool(6)
        start_time = time.time()
        listaLinks = []
        #Definir estrutura do dataframe
        '''
        colunas = ['cargo/função', 'Salário','-', 'Localização','-', 'atribuição', 'Benefícios', '-', 'tipo de vinculo', '-','Descrição geral']
        '''
        colunas = ['Url','Codigo','Vaga', 'Salário','Vagas', 'Localidade','Data', 'Conteúdo', 'Benefícios', 'Horário', 'Regime', 'Adicional','Dados da empresa']
        df = definirDataframe(colunas)

        #Quantas paginas existem
        #paginas = BnePage.obterQuantidaDePaginasEncontradas("//h1[@class='job__list__title']/strong")
        #print('paginas', paginas)
        #Percorrer Pagina e obter links
        for i in range(1,2001):
            print(i)
            links = []
            r = requests.get('https://www.bne.com.br/vagas-de-emprego/?Page=%s'% i)
            links = receberlistaDeVagasQueExistemNaPaginaVagaCertaScrapy(r)

            for el in range(len(links)):
                listaLinks.append(links[el])

            # Acessar links e obter conteudo
        for il in listaLinks:
            a = "https://www.bne.com.br" + il
            r = requests.get(a)
            df = obterConteudoDaPaginaScrapy(df, r,a)

        #Acessar links e obter conteudo


        #exportar em csv
        #nome_xls = localidade + '.csv'
        nome_xls = 'bneScrapy.csv'
        exportarCsv(df,nome_xls)

    except:
        print('Erro no Programa!', sys.exc_info()[0])
        print("--- %s seconds ---" % (time.time() - start_time))
        raise
    finally:
        # fim = time.time()
        print("--- %s seconds ---" % (time.time() - start_time))
        print("Finalizado")



