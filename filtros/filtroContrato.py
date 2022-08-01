from multiprocessing.sharedctypes import Value
from shutil import ExecError
from time import strftime
import urllib.request
from bs4 import BeautifulSoup
from datetime import date
import pandas as pd
import numpy as np

I_DATA = '01/01/2022'
F_DATA = date.today().strftime("%d/%m/%Y")
URL_CONTRATO = str(f"http://www.governotransparente.com.br/acessoinfo/44669490/consultarcontratoaditivo?ano=5&credor=-1&page=1&datainfo=%22MTIwMjIwNTIwMDkzOFBQUA==%22&inicio={I_DATA}&fim={F_DATA}&unid=&valormax=&valormin=")
NUM_CONTRATO = []
CONTRATOS_SEM_ANEXO = []

def itensCount():
    global totalContratos
    page = urllib.request.urlopen(URL_CONTRATO)
    soup = BeautifulSoup(page, 'html5lib')

    TOTAL = []
    tabela = soup.find_all('p')
    for p in tabela:
        TOTAL.append(p)
    total = str(TOTAL[0]).split()
    totalContratos = int(total[6])
    return totalContratos

def pageCount():
    global totalPages
    if (totalContratos % 10) == 0:
        totalPages = (totalContratos // 10)
    else:
        totalPages = ((totalContratos // 10) + 1)
    return totalPages

def crawlingData():
    itensCount()
    pageCount()
    for pag in range(1, totalPages + 1):
        global URL_CONTRATO
        newPage = f"page={pag}"
        URL_CONTRATO = URL_CONTRATO.replace(f'page={pag - 1}', newPage)

        # Acessando Página
        page = urllib.request.urlopen(URL_CONTRATO)
        soup = BeautifulSoup(page, 'html5lib')

        # Procurando Tabela
        table = soup.find('table', class_ = 'table')
        
        # Retirando infos da tabela:
        for row in table.findAll('tr'):
            cells = row.findAll('td')
            if len(cells) == 10:
                NUM_CONTRATO.extend([[
                    cells[0].find(text=True),
                    cells[1].find(text=True),
                int(cells[8].find(text=True))
                ]])
        print(f"{(pag / (totalPages)) * 100:.2f}% completados")
def filtroSemAnexo():
    # Filtrando contratos sem anexo
    for innerList in NUM_CONTRATO:
        if innerList[2] == 0:
            CONTRATOS_SEM_ANEXO.append(innerList)
        else:
            continue

def excelCreator():
    # Escrevendo os dados coletados em uma Planilha
    array = np.array(CONTRATOS_SEM_ANEXO)
    df = pd.DataFrame(array)
    df.to_excel(excel_writer='CONTRATOS.xlsx', index=False,sheet_name='CONTRATOS',header=['data cadastrada','n. do contrato','total de anexos'])

def main():

    print('Filtro de Contratos Iniciado\n')
    crawlingData()
    filtroSemAnexo()
    excelCreator()
    print('\nFiltro de Contratos Finalizado\n')

if __name__ == '__main__':
    try:
        main()
    except ValueError as e:
        print(e)