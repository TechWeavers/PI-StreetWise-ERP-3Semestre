from fastapi import APIRouter, FastAPI, Depends,Header
from routes.loginRoute import validar_token
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from models.clienteModel import Cliente
from Controllers.Controller_Cliente import ControllerCliente

app = FastAPI()
clienteAPI = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)
# CRUD de clientes e ficha de anamnese funcionando por completo ja

@clienteAPI.post("/novo-cliente", tags=["clientes"])
async def createUser(cli:Cliente, Authorization: Annotated[Header, Depends(validar_token)]): #
    return ControllerCliente.insertCliente(cli)

@clienteAPI.get("/listar-clientes", tags=["clientes"])
async def listarClientes(Authorization: Annotated[Header, Depends(validar_token)]):
     print(Authorization)
     return ControllerCliente.getAllClientes()

@clienteAPI.get("/buscar-cliente/{cpf}", tags=["clientes"]) 
async def buscarUsuario(cpf:str, Authorization: Annotated[Header, Depends(validar_token)]):
    return ControllerCliente.getCliente(cpf)

@clienteAPI.get("/editar-cliente/{cpf}", tags=["clientes"])
async def editarUsuario(cpf:str, Authorization: Annotated[Header, Depends(validar_token)]):
     cliente = ControllerCliente.getCliente(cpf)
     return cliente # para carregar os dados do usuário encontrado na página de atualizar dados

@clienteAPI.patch("/atualizar-cliente/{cpf}", tags=["clientes"]) 
async def atualizarCliente(cliente:Cliente, cpf:str ,Authorization: Annotated[Header, Depends(validar_token)]):
     return ControllerCliente.updateCliente(dict(cliente), cpf)

@clienteAPI.delete("/deletar-cliente/{cpf}", tags=["cliente"])
async def excluirCliente(cpf:str, Authorization: Annotated[Header, Depends(validar_token)]):
     return ControllerCliente.deleteCliente(cpf)

@clienteAPI.patch("/atualizar-ficha/{cpf}", tags=["clientes"]) 
async def atualizarFicha(ficha_data:dict,cpf:str, Authorization: Annotated[Header, Depends(validar_token)]):
     Controller = ControllerCliente()
     return Controller.salvarFicha(ficha_data, cpf)



app.include_router(clienteAPI)
