from fastapi import APIRouter, FastAPI, Depends,Header
from routes.loginRoute import validar_token
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
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
async def buscar_materiais_faltantes(Authorization: Annotated[Header, Depends(validar_token)]):
  return ControllerMaterial.CalcularMateriaisFaltantes()

@relatorioAPI.get("/proximos-agendamentos", tags=["relatorios"])
async def buscar_proximos_agendamentos(Authorization: Annotated[Header, Depends(validar_token)]):
  return Controller_Copia_Agendamento.calcularProximosAgendamentos()

@relatorioAPI.get("/quantidade-agendamentos", tags=["relatorios"])
async def buscar_quantidade_agendamentos_no_mes(Authorization: Annotated[Header, Depends(validar_token)]):
  controller = Controller_Copia_Agendamento()
  return controller.calcularQuantidadeAgendamentosnoMes()

@relatorioAPI.get("/valorBruto-agendamentos", tags=["relatorios"])
async def buscar_valor_bruto_agendamentos_no_mes(Authorization: Annotated[Header, Depends(validar_token)]):
  controller = Controller_Copia_Agendamento()
  return controller.valorAgendamentosNoMes()

@relatorioAPI.get("/media-agendamentos", tags=["relatorios"])
async def buscar_media_agendamentos_no_mes(Authorization: Annotated[Header, Depends(validar_token)]):
  controller = Controller_Copia_Agendamento()
  return controller.media_valor_agendamentos_no_mes()

app.include_router(relatorioAPI)