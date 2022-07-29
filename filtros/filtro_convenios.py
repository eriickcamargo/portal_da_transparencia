from cgitb import text
from operator import index
import time
import urllib.request
from xml.etree import cElementTree
from bs4 import BeautifulSoup
import csv
from datetime import date
import ezgmail
import pandas as pd
import numpy as np

#Declarando Variáveis Globais

I_DATA = '01/01/2022'
F_DATA = date.today().strftime("%d/%m/%Y")
URL_CONVENIOS = str(f"http://www.governotransparente.com.br/transparencia/44669490/consultarconvenio?page=1&datainfo=%22MTIwMjIwNzI5MTM1MFBQUA==%22&inicio={I_DATA}&fim={F_DATA}&iniciovi=&fimvi=&iniciovi2=&fimvi2=")
NUM_CONVENIOS = []
CONVENIOS_SEM_ANEXO = []

def itensCount():
    global quantTotalConvenios
    page =  urllib.request.urlopen(URL_CONVENIOS)
    soup = BeautifulSoup(page, 'html5lib')

    TOTAL = []
    tabela = soup.find_all('p')
    for p in tabela:
        TOTAL.append(p)
    total = str(TOTAL[0]).split()
    quantTotalConvenios = int(total[6]) #quantidade total de convenios em aberto no portal
    return quantTotalConvenios


def pageCount():
    global totalPages
    if (quantTotalConvenios % 10) == 0:
        totalPages = ((quantTotalConvenios // 10))
        #print(totalPages, 'se o resto for zero')
    else:
        totalPages = ((quantTotalConvenios // 10) + 1)
        #print(totalPages, 'se o resto for > 0')

def crawlingData():
    itensCount()
    pageCount()
    
    for pag in range(1, totalPages + 1):
        global URL_CONVENIOS
        newPage = f"page={pag}"
        URL_CONVENIOS = URL_CONVENIOS.replace(f'page={pag - 1}', newPage)
        #print(URL_CONVENIOS, 'segundo if', pag)
        
        # Acessando Página
        page = urllib.request.urlopen(URL_CONVENIOS)
        soup = BeautifulSoup(page, 'html5lib')

        # Procurando tabela
        table = soup.find('table',  class_= 'table')

        # Crawling
        for row in table.findAll('tr'):
            cells = row.findAll('td')
            if len(cells) == 9:
                NUM_CONVENIOS.extend([[
                cells[0].find(text=True), 
                cells[1].find(text=True), 
                int(cells[7].find(text=True))]])
    #print(NUM_CONVENIOS)
def filtroSemAnexo():
    for innerList in NUM_CONVENIOS:
        if innerList[2] == 0:
            CONVENIOS_SEM_ANEXO.append(innerList)
        else:
            continue

def excelCreator():
    array = np.array(CONVENIOS_SEM_ANEXO)
    df = pd.DataFrame(array)
    df.to_excel(excel_writer='my_excel_test.xlsx', index=False,sheet_name='CONVENIOS',header=['data','n. do convenio','total de anexos'])

#def sendEmail():
#    try:
#        emailBody = f"Bom dia, \nAqui está a relação de convênios sem anexo no Portal da Transparência, foram encontrados no total {len(CONVENIOS_SEM_ANEXO)} convenios sem anexo, até amanhã!"
#        ezgmail.send('ericklimacamargo@gmail.com', 'Relação de Contratos Sem Anexo', emailBody, ['my_excel_test.xlsx'], 'Erick Automate', None,)
#    except Exception as emailError:
#        print(f"Houve um erro ao enviar o e-mail: {emailError}")

try:
    start = time.time()
    crawlingData()
    filtroSemAnexo()
    excelCreator()
    sendEmail()
    stop = time.time()

except Exception as e:
    print(e)

