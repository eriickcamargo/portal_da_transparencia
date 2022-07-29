import ezgmail
import time
import filtros
from filtros import filtroContrato
from filtros import filtroConvenios

def sendEmail():
    try:
        emailBody = f"Bom dia, \nAqui está a resultado da varredura no Portal da Transparência, até amanhã!"
        ezgmail.send('ericklimacamargo@gmail.com', 'Pendências do Portal da Transparência', emailBody, ['CONTRATOS.xlsx','CONVENIOS.xlsx'], 'Erick Automate', None,)
    except Exception as emailError:
        print(f"Houve um erro ao enviar o e-mail: {emailError}")

def main():
    start_timer = time.time() 

    #Filtro de Convenios
    filtroConvenios.main()

    #Filtro de Contratos:
    filtroContrato.main()

    #Envia e-mail
    #sendEmail()
    end_timer = time.time()
    print(f"Foram necessários {end_timer - start_timer:.2f} segundos")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)