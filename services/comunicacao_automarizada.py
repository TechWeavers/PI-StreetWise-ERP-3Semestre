import schedule
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from services import email
from Controllers.Controller_Agenda import Controller_Copia_Agendamento


def enviar_email(): # Agendar o envio do e-mail todos os dias às 01:30 da madrugada
  controller = Controller_Copia_Agendamento()
  agendamentos = controller.retornar_todos_agendamentos()

  for event in agendamentos:
      return True
  schedule.every().day.at("01:30").do(email.email24Antes())

  

# Loop para verificar a agenda e executar as funções agendadas
def verifica_agenda():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # Iniciar o temporizador
    verifica_agenda()
