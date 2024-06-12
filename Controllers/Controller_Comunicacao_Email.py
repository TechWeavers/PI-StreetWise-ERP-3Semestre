from datetime import datetime, timedelta
from Controllers.Controller_Agenda import Controller_Copia_Agendamento
from services.email import email24Depois, email24Antes, emailRetorno
from fastapi import FastAPI, APIRouter, HTTPException, status

class Controller_Email:
  def __init__(self):
    pass

  async def enviar_email_24_horas_depois(self):
    try:
        controller = Controller_Copia_Agendamento()
        agendamentos = controller.retornar_todos_agendamentos()

        # Obter a data atual
        data_atual = datetime.now()

        # Subtrair um dia da data atual para obter a data de ontem
        data_ontem = data_atual - timedelta(days=1)

        # Formatar a data de ontem no mesmo formato do objeto JSON
        data_ontem = data_ontem.strftime('%Y-%m-%dT%H:%M:%S')
        data_ontem = data_ontem[:10]
        data_ontem_formatada = str(data_ontem)

        for event in agendamentos:
            data_evento = str(event["start"]["dateTime"]).split("T")[0]

            print("data do evento",data_evento)
            print("data de ontem",data_ontem_formatada)
            if data_evento == data_ontem_formatada:
              email_cliente = event["attendees"][0]["email"]
              await email24Depois(email_cliente)
              print("deu certo")
            else:
                print("nao deu certo")
                
    except Exception:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Não foram encontrados agendamentos nda data de ontem")
    
  async def enviar_email_24_horas_antes(self):
    try:
        controller = Controller_Copia_Agendamento()
        agendamentos = controller.retornar_todos_agendamentos()

        # Obter a data atual
        data_atual = datetime.now()

        # Subtrair um dia da data atual para obter a data de ontem
        data_amanha = data_atual + timedelta(days=1)

        # Formatar a data de ontem no mesmo formato do objeto JSON
        data_amanha = data_amanha.strftime('%Y-%m-%dT%H:%M:%S')
        data_amanha = data_amanha[:10]
        data_amanha_formatada = str(data_amanha)

        for event in agendamentos:
            data_evento = str(event["start"]["dateTime"]).split("T")[0]

            print(data_evento)
            print(data_amanha_formatada)
            if data_evento == data_amanha_formatada:
              email_cliente = event["attendees"][0]["email"]
              await email24Antes(email_cliente)
            else:
                print("nao deu certo")
                
          
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Não foram encontrados agendamentos na data de amanhã")
    