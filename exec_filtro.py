from filtros.filtro_convenios import *

def sendEmail():
    try:
        emailBody = f"Bom dia, \nAqui está a relação de convênios sem anexo no Portal da Transparência, foram encontrados no total {len(CONVENIOS_SEM_ANEXO)} convenios sem anexo, até amanhã!"
        ezgmail.send('ericklimacamargo@gmail.com', 'Relação de Contratos Sem Anexo', emailBody, ['my_excel_test.xlsx'], 'Erick Automate', None,)
    except Exception as emailError:
        print(f"Houve um erro ao enviar o e-mail: {emailError}")

crawlingData()
filtroSemAnexo()
excelCreator()
sendEmail()