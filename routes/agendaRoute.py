from fastapi import APIRouter, FastAPI, Depends,Header
from routes.loginRoute import validar_token, validar_token_admin
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from Controllers.Controller_Agenda import AgendaController

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
async def createAgendamento(agenda_data: agenda, Authorization: Annotated[Header, Depends(validar_token)]): #
    return AgendaController.insertAgenda(agenda_data)

@agendaAPI.get("/listar-agendamentos", tags=["agendamentos"])
async def listarMateriais(Authorization: Annotated[Header, Depends(validar_token)]):
     return AgendaController.getAllAgenda()

@agendaAPI.patch("/atualizar-agendamento/{agendaid}", tags=["agendamentos"]) 
async def atualizarCliente(agenda_data: agenda, nome:str ,Authorization: Annotated[Header, Depends(validar_token)]):
     return AgendaController.updateAgenda(dict(agenda_data), nome)

@agendaAPI.delete("/deletar-agendamento/{agendaid}", tags=["agendamentos"])
async def excluirMaterial(agendaid:str, Authorization: Annotated[Header, Depends(validar_token)]):
     return AgendaController.deleteAgenda(agendaid)

app.include_router(agendaAPI)


