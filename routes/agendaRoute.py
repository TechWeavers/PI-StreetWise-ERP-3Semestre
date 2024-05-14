from fastapi import APIRouter, FastAPI, Depends,Header
from routes.loginRoute import validar_token, validar_token_admin
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
#from Controllers.Controller_Agenda import AgendaController
from GoogleCalendarAPI.GoogleCalendar import GoogleCalendar
from models.agendamentoModel import Agendamento


app = FastAPI()
agendaAPI = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

@agendaAPI.post("/novo-agendamento", tags=["agendamentos"])
async def createAgendamento(evento:Agendamento): #agenda_data: dict,Authorization: Annotated[Header, Depends
    controller = GoogleCalendar()
    return controller.insert_event(evento)

"""@agendaAPI.get("/listar-agendamentos", tags=["agendamentos"])
async def listarMateriais(Authorization: Annotated[Header, Depends(validar_token)]):
     return AgendaController.getAllAgenda()

#@agendaAPI.patch("/atualizar-agendamento/{agendaid}", tags=["agendamentos"]) 
#async def atualizarCliente(agenda_data: agenda, nome:str ,Authorization: Annotated[Header, Depends(validar_token)]):
     #return AgendaController.updateAgenda(dict(agenda_data), nome)
"""
@agendaAPI.delete("/deletar-agendamento/{event_ID}", tags=["agendamentos"])
async def excluirMaterial(event_ID:str):#, Authorization: Annotated[Header, Depends(validar_token)]
     controller = GoogleCalendar()
     return controller.deleteAgenda(event_ID)

app.include_router(agendaAPI)


