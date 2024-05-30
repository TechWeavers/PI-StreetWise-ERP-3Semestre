from fastapi import APIRouter, FastAPI, Depends,Header
from routes.loginRoute import validar_token
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from models.clienteModel import Cliente
from Controllers.Controller_Material import ControllerMaterial
from Controllers.Controller_Agenda import Controller_Copia_Agendamento

app = FastAPI()
relatorioAPI = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

@relatorioAPI.get("/materiais-faltantes", tags=["relatorios"])
async def buscarMateriaisFaltantes():
  return ControllerMaterial.CalcularMateriaisFaltantes()

@relatorioAPI.get("/proximos-agendamentos", tags=["relatorios"])
async def buscarProximosagendamentos():
  return Controller_Copia_Agendamento.calcularProximosAgendamentos()

@relatorioAPI.get("/quantidade-agendamentos", tags=["relatorios"])
async def buscarProximosagendamentos():
  controller = Controller_Copia_Agendamento()
  return controller.calcularQuantidadeAgendamentosnoMes()

app.include_router(relatorioAPI)