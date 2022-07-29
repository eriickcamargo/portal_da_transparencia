import urllib.request
from bs4 import BeautifulSoup
import csv
import ctypes
from datetime import date
import ezgmail

#DECLARADO VARIÁVEIS GLOBAIS

I_DATA = '01/01/2022'
F_DATA = date.today()
F_DATA2 = str(F_DATA.strftime("%d/%m/%Y"))
print(F_DATA2)

URL_TRANSP = str(f"http://www.governotransparente.com.br/acessoinfo/44669490/consultarcontratoaditivo?ano=5&credor=-1&page=1&datainfo=%22MTIwMjIwNTIwMDkzOFBQUA==%22&inicio={I_DATA}&fim={F_DATA2}&unid=&valormax=&valormin=")
NUM_CONTRATO = []
print(URL_TRANSP)
try:
    #Acessando a Página
    page = urllib.request.urlopen(URL_TRANSP)
    soup = BeautifulSoup(page,'html5lib')
    
    #Procurando quantidade de páginas
    TOTAL = []
    tabela = soup.find_all('p')
    for p in tabela:
        TOTAL.append(p)
    total = str(TOTAL[0]).split()
    quant_TOTAL_i = int(total[6]) #quantidade total de contratos
    
    if (quant_TOTAL_i % 10) == 0:
        quant_TOTAL_pag = ((quant_TOTAL_i // 10) + 1)
    else:
        quant_TOTAL_pag = ((quant_TOTAL_i // 10) + 2) #quantidade total de páginas a serem checadas

except:
    ctypes.windll.user32.MessageBoxW(0, f"As ações preliminares de levantamento de dados deram errado. Precione OK para fechar o programa.\n", "ERRO", 1)    

#Levantando Dados a partir da página do Portal da Transparência
try:
    for i in range(1 , quant_TOTAL_pag):
        b = f"page={i}"
        new_URL_TRANSP = URL_TRANSP.replace('page=1', b )

        #Acessando a página
        page = urllib.request.urlopen(new_URL_TRANSP)
        soup = BeautifulSoup(page, 'html5lib')

        #Procura a tabela
        table = soup.find('table', class_ = 'table')

        #Retira as informações da tabela
        for row in table.findAll('tr'):
            cells = row.findAll('td')
            if len(cells) == 10:
                NUM_CONTRATO.extend([[cells[1].find(text=True), int(cells[8].find(text=True))]])
        print(f"Estou colhendo os dados, restam {quant_TOTAL_pag - i} páginas para serem análisadas.")

except:
    ctypes.windll.user32.MessageBoxW(0, f"O processo de levantamento de dados foi abortado automaticamente por um erro interno. Precione OK para fechar o programa.\n", "ERRO", 1)


#Filtrando por apenas contratos sem anexos
CONTRATOS_SEM_ANEXO = []
try:
    for num_contrato in NUM_CONTRATO:
        if num_contrato[1] == 0:
            CONTRATOS_SEM_ANEXO.append(num_contrato[0])
        else:
            continue
except:
    ctypes.windll.user32.MessageBoxW(0, f"O processo de filtro foi abortado automaticamente por um erro interno\nPrecione OK para fechar o programa.\n", "ERRO", 1)


#Escreve os dados em um arquivo CSV

if len(CONTRATOS_SEM_ANEXO) == 0:
    ctypes.windll.user32.MessageBoxW(0, f"Não foram encontrados contratos sem anexo! \nPrecione OK para fechar o programa.", "FINALIZADO", 1)

else:
    #archive_name = f"{I_DATA.replace('/','_')} a {F_DATA.replace('/','_')}.csv"

    with open('relacao_contratos.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(zip(CONTRATOS_SEM_ANEXO))
    
<<<<<<< HEAD
    ctypes.windll.user32.MessageBoxW(0, f"Processo finalizado, foram localizados {len(CONTRATOS_SEM_ANEXO)} contratos sem anexos.\n", "FINALIZADO", 1)
=======
#    ctypes.windll.user32.MessageBoxW(0, f"Processo finalizado, foram localizados {len(CONTRATOS_SEM_ANEXO)} contratos sem anexos.\n", "FINALIZADO", 1)
>>>>>>> 4134698fb1dbc1229c93e1ecf10582f6d7cf59d8
