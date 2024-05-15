from fastapi import APIRouter, FastAPI, Depends,Header
from routes.loginRoute import validar_token, validar_token_admin
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
#from Controllers.Controller_Agenda import AgendaController
from GoogleCalendarAPI.GoogleCalendar import GoogleCalendar
from models.agendamentoModel import Agendamento
from Controllers.Controller_Agenda import Controller_Copia_Agendamento

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

@agendaAPI.get("/listar-agendamentos", tags=["agendamentos"])
async def listarAgendamentos():#Authorization: Annotated[Header, Depends(validar_token)]
     return Controller_Copia_Agendamento.getAllAgendamentos()

@agendaAPI.put("/atualizar-agendamento/{eventoId}", tags=["agendamentos"]) 
async def atualizarCliente(eventoId: str, evento:Agendamento ):#,Authorization: Annotated[Header, Depends(validar_token)]
     controller = GoogleCalendar()
     return controller.updateAgendamento(eventoId,dict(evento))

@agendaAPI.delete("/deletar-agendamento/{event_ID}", tags=["agendamentos"])
async def excluirMaterial(event_ID:str):#, Authorization: Annotated[Header, Depends(validar_token)]
     controller = GoogleCalendar()
     return controller.deleteAgenda(event_ID)

app.include_router(agendaAPI)


