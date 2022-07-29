from filtros import *
from filtros import filtro_convenios
import ezgmail

def sendEmail():
    try:
        emailBody = f"Bom dia, \nAqui está a resultado da varredura no Portal da Transparência, até amanhã!"
        ezgmail.send('ericklimacamargo@gmail.com', 'Pendências do Portal da Transparência', emailBody, ['my_excel_test.xlsx'], 'Erick Automate', None,)
    except Exception as emailError:
        print(f"Houve um erro ao enviar o e-mail: {emailError}")

#Filtro de Convenios
filtro_convenios.crawlingData()
filtro_convenios.filtroSemAnexo()
filtro_convenios.excelCreator()

#Filtro de Contratos:

sendEmail()
