from multiprocessing.sharedctypes import Value
from re import sub
import ezgmail
import time
from filtros import filtroContrato
from filtros import filtroConvenios
from filtros import filtroLicitacao

def sendEmail():
    try:
        emailBody = f"Bom dia, \nAqui está a resultado da varredura no Portal da Transparência, até amanhã!"
        title = f"Portal da Transparência - Pendências"
        attachments = ['CONTRATOS.xlsx']
        bcc = 'seplan@maraba.pa.gov.br,contratos.seplan@maraba.pa.gov.br'

        ezgmail.send(recipient='ericklimacamargo@gmail.com',
        subject=title,
        body=emailBody,
        attachments=attachments,
        sender= 'Erick Automated',
        bcc=bcc)

        # ezgmail.send('ericklimacamargo@gmail.com',
        # 'Pendências do Portal da Transparência',
        # emailBody,
        # ['CONTRATOS.xlsx','CONVENIOS.xlsx','LICITACOES.xlsx']
        # , 'Erick Automate',
        # None,)
    except ValueError as emailError:
        print(f"Houve um erro ao enviar o e-mail: {emailError}")

def main():
    start_timer = time.time() 

    #Filtro de Convenios
    #filtroConvenios.main()

    #Filtro de Contratos:
    filtroContrato.main()

    # Filtro de Licitações
    #filtroLicitacao.main()

    #Envia e-mail
    sendEmail()
    end_timer = time.time()
    print(f"Foram necessários {end_timer - start_timer:.2f} segundos")

if __name__ == '__main__':
    try:
        main()
    except ValueError as e:
        print(e)