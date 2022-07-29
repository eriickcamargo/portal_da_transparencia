from shutil import ExecError
from time import strftime
import urllib.request
from bs4 import BeautifulSoup
import csv
from datetime import date
import ezgmail

I_DATA = '01/01/2022'
F_DATA = date.today().strftime("%d/%m/%Y")
URL_TRANSP = str(f"http://www.governotransparente.com.br/acessoinfo/44669490/consultarcontratoaditivo?ano=5&credor=-1&page=1&datainfo=%22MTIwMjIwNTIwMDkzOFBQUA==%22&inicio={I_DATA}&fim={F_DATA}&unid=&valormax=&valormin=")
NUM_CONTRATO = []
CONTRATOS_SEM_ANEXO = []

try:
    page = urllib.request.urlopen(URL_TRANSP)
    soup = BeautifulSoup(page, 'html5lib')

    TOTAL = []
    tabela = soup.find_all('p')
    for p in tabela:
        TOTAL.append(p)
    total = str(TOTAL[0]).split()
    quant_TOTAL_i = int(total[6])
    
    if (quant_TOTAL_i % 10) == 0:
        quant_TOTAL_pag = ((quant_TOTAL_i // 10) + 1)
    else:
        quant_TOTAL_pag = ((quant_TOTAL_i // 10) + 1)

    for i in range (1, quant_TOTAL_pag):
        b = f"page={i}"
        new_URL_TRANSP = URL_TRANSP.replace('page=1', b)

        # Acessando Página
        page = urllib.request.urlopen(new_URL_TRANSP)
        soup = BeautifulSoup(page, 'html5lib')

        # Procurando Tabela
        table = soup.find('table', class_ = 'table')
        
        # Retirando infos da tabela:
        for row in table.findAll('tr'):
            cells = row.findAll('td')
            if len(cells) == 10:
                NUM_CONTRATO.extend([[cells[1].find(text=True), int(cells[8].find(text=True))]])
        print(f"Estou colhendo os dados, restam {quant_TOTAL_pag - i} páginas para serem análisadas.")
    
    # Filtrando contratos sem anexo
    for num_contrato in NUM_CONTRATO:
        if num_contrato[1] == 0:
            CONTRATOS_SEM_ANEXO.append(num_contrato[0])
        else:
            continue
    
    # Escrevendo os dados coletados em um arquivo CSV
    if len(CONTRATOS_SEM_ANEXO) == 0:
        print(f"Não foram encontrados contratos sem anexo!")
    else:
        with open('relacao_contratos.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerows(zip(CONTRATOS_SEM_ANEXO))
        f.close()
    
    try:
        emailBody = f"Bom dia, \nAqui está a relação de contratos sem anexo no Portal da Transparência, foram encontrados no total {len(CONTRATOS_SEM_ANEXO)} contratos sem anexo, até amanhã!"
        ezgmail.send('ericklimacamargo@gmail.com', 'Relação de Contratos Sem Anexo', emailBody, ['relacao_contratos.csv'], 'Erick Automate', None, 'seplan@maraba.pa.gov.br,contratos.seplan@maraba.pa.gov.br')
    except Exception as emailError:
        print(f"Houve um erro ao enviar o e-mail: {emailError}")

except Exception as e:
    print(e)