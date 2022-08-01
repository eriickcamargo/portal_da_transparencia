from shutil import ExecError
from time import strftime
from tkinter import N
import urllib.request
from bs4 import BeautifulSoup
from datetime import date
import pandas as pd
import numpy as np

I_DATA = '01/01/2022'
F_DATA = date.today().strftime("%d/%m/%Y")
URL_LICITACAO = str(f"http://www.governotransparente.com.br/transparencia/44669490/consultarlicitacao?page=1&datainfo=%22MTIwMjIwODAxMTMzMFBQUA==%22&inicio={I_DATA}&fim={F_DATA}&iniciovi=&fimvi=&iniciovi2=&fimvi2=")
NUM_LICITACAO = []
LICITACOES_SEM_ANEXO = []

def itensCount():
    global totalLicitacoes
    page = urllib.request.urlopen(URL_LICITACAO)
    soup = BeautifulSoup(page, 'html5lib')

    TOTAL = []
    tabela = soup.find_all('p')
    for p in tabela:
        licitacoes = str(tabela[0]).split()
        totalLicitacoes = int(licitacoes[6])
    
    return totalLicitacoes

def pageCount():
    global totalPages
    if (totalLicitacoes % 10) == 0:
        totalPages = (totalLicitacoes // 10)
    else:
        totalPages = ((totalLicitacoes // 10) + 1)
    return totalPages

def crawlingData():
    global URL_LICITACAO

    itensCount()
    pageCount()
    for pag in range(1, totalPages + 1):
        newPage = f"page={pag}"
        URL_LICITACAO = URL_LICITACAO.replace(f"page={pag - 1}", newPage)

        # Acessando Página
        page = urllib.request.urlopen(URL_LICITACAO)
        soup = BeautifulSoup(page, 'html5lib')

        # Procurando Tabela
        table = soup.find('table', class_ = 'table')

        # Crawling Data
        for row in table.findAll('tr'):
            cells = row.findAll('td')
            if len(cells) == 9:
                NUM_LICITACAO.extend([[
                    cells[2].find(text=True), # Data
                    cells[0].find(text=True), # Numero da Licitacao
                    int(cells[7].find(text=True)) # Numero e Anexos
                ]])
        print(f"{(pag / (totalPages)) * 100:.2f}% completados")

def filtroSemAnexo():
    # Filtrando contratos sem anexo
    for innerList in NUM_LICITACAO:
        if innerList[2] <= 5:
            LICITACOES_SEM_ANEXO.append(innerList)
        else:
            continue
    print(LICITACOES_SEM_ANEXO)

def excelCreator():
    # Escrevendo os dados coletados em um Planilha Excel
    array = np.array(LICITACOES_SEM_ANEXO)
    df = pd.DataFrame(array)
    df.to_excel(excel_writer='LICITACOES.xlsx', index=False, sheet_name='Licitações', header= ['data de abertura', 'n. da licitação', 'total de anexos'])

def main():
    print('Filtro de Licitações Iniciado\n')
    crawlingData()
    filtroSemAnexo()
    excelCreator()
    print('\nFiltro de Licitações Finalizado')

if __name__ == '__main__':
    try:
        main()
    except ValueError as e:
        print(e)