from fastapi import APIRouter, FastAPI, Depends,Header
from routes.loginRoute import validar_token
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from models.clienteModel import Cliente
from Controllers.Controller_Cliente import ControllerCliente

app = FastAPI()
userAPI = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

@userAPI.post("/novo-cliente", tags=["clientes"])
async def createUser(cli:Cliente, Authorization: Annotated[Header, Depends(validar_token)]): #
    return ControllerCliente.insertCliente(cli)

@userAPI.get("/listar-clientes", tags=["clientes"])
async def listarClientes(Authorization: Annotated[Header, Depends(validar_token)]):
     print(Authorization)
     return ControllerCliente.getAllClientes()

@userAPI.get("/buscar-cliente/{cpf}", tags=["clientes"]) 
async def buscarUsuario(cpf:str, Authorization: Annotated[Header, Depends(validar_token)]):
    return ControllerCliente.getCliente(cpf)

@userAPI.get("/editar-cliente/{cpf}", tags=["clientes"])
async def editarUsuario(cpf:str, Authorization: Annotated[Header, Depends(validar_token)]):
     cliente = ControllerCliente.getCliente(cpf)
     return cliente # para carregar os dados do usuário encontrado na página de atualizar dados

@userAPI.patch("/atualizar-cliente/{cpf}", tags=["clientes"]) 
async def atualizarCliente(cliente:Cliente, cpf:str ,Authorization: Annotated[Header, Depends(validar_token)]):
     return ControllerCliente.updateCliente(dict(cliente), cpf)

@userAPI.delete("/deletar-cliente/{cpf}", tags=["cliente"])
async def excluirCliente(cpf:str, Authorization: Annotated[Header, Depends(validar_token)]):
     return ControllerCliente.deleteCliente(cpf)

app.include_router(userAPI)
