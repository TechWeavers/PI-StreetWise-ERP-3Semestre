from fastapi import APIRouter, FastAPI, Depends,Header
from routes.loginRoute import validar_token
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from models.userModel import User
#importando controllers
from Controllers.Controller_user import ControllerUser

app = FastAPI()
userAPI = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@userAPI.post("/novo-usuario", tags=["usuarios"])
async def createUser(user:User, Authorization: Annotated[Header, Depends(validar_token)]):
     return ControllerUser.insertUser(user)

@userAPI.get("/listar-usuarios", tags=["usuarios"])
async def listarUsuarios():
     return ControllerUser.getAllUsers()

@userAPI.get("/buscar-usuario/{email}", tags=["usuarios"]) 
async def buscarUsuario(email:str):
     return ControllerUser.getUser(email)
# buscando um usuario por email, pois é atributo unico

@userAPI.get("/editar-usuario/{email}", tags=["usuarios"])
async def editarUsuario(email:str):
     user = ControllerUser.getUser(email) # busca o usuário para atualizar
     return user # para carregar os dados do usuário encontrado na página (spa) de atualizar dados

@userAPI.patch("/atualizar-usuario", tags=["usuarios"]) 
async def atualizarUsuario(user:User):
     return ControllerUser.updateUser(dict(user))
# atualiza o usuario passando um objeto usuario no corpo da requisição, e chama a função de update, enviando os dados de atualização no corpo da requisição

@userAPI.delete("/deletar-usuario/{email}", tags=["usuarios"])
async def excluirUsuarios(email:str):
     return ControllerUser.deleteUser(email)

app.include_router(userAPI)