from http.client import HTTPException
from fastapi import Depends, FastAPI, Header,APIRouter
from pydantic import BaseModel
from starlette.responses import JSONResponse
from routes.loginRoute import validar_token
from services.email import EmailSchema, emailEsqueceuSenha
from Controllers.Controller_user import ControllerUser
from fastapi.middleware.cors import CORSMiddleware
from Controllers.token import Token
from Controllers.Controller_Agenda import Controller_Copia_Agendamento
from datetime import datetime, timedelta
from typing import Annotated
from models.emailModel import emailClass
from models.senhaModel import SenhaClass
from services.email import email24Depois,email24Antes,emailRetorno

app = FastAPI()
comunicacaoAPI = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

@app.post("/email-24horas-depois")
async def enviar_email_24_horas_depois(): 
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

            print(data_evento)
            print(data_ontem_formatada)
            if data_evento == data_ontem_formatada:
              email_cliente = event["attendees"][0]["email"]
              await email24Depois(email_cliente)
           
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(500, f"Erro ao enviar o e-mail: {str(e)}")
    
@app.post("/email-24horas-antes")
async def enviar_email_24_horas_antes(): 
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
           
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(500, f"Erro ao enviar o e-mail: {str(e)}")
    

@app.post("/email-retorno")
async def enviar_email_retorno(): 
    try:
        controller = Controller_Copia_Agendamento()
        agendamentos = controller.retornar_todos_agendamentos()

        # Obter a data atual
        data_atual = datetime.now()

        # Subtrair um dia da data atual para obter a data de ontem
        data_retorno = data_atual + timedelta(days=15)

        # Formatar a data de ontem no mesmo formato do objeto JSON
        data_retorno = data_retorno.strftime('%Y-%m-%dT%H:%M:%S')
        data_retorno = data_retorno[:10]
        data_retorno_formatada = str(data_retorno_formatada)

        for event in agendamentos:
            data_evento = str(event["start"]["dateTime"]).split("T")[0]

            if data_evento == data_retorno_formatada:
              email_cliente = event["attendees"][0]["email"]
              await emailRetorno(email_cliente)
           
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(500, f"Erro ao enviar o e-mail: {str(e)}")

app.include_router(comunicacaoAPI)