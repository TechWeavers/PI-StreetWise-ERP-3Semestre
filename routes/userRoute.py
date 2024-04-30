from fastapi import APIRouter, FastAPI, Depends,Header
from routes.loginRoute import validar_token,validar_token_admin
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
async def createUser(user:User, Authorization: Annotated[Header, Depends(validar_token_admin)]):
     return ControllerUser.insertUser(user)

@userAPI.get("/listar-usuarios", tags=["usuarios"])
async def listarUsuarios(Authorization: Annotated[Header, Depends(validar_token)]):
     print(Authorization)
     return ControllerUser.getAllUsers()

@userAPI.get("/buscar-usuario/{email}", tags=["usuarios"]) 
async def buscarUsuario(email:str, Authorization: Annotated[Header, Depends(validar_token)]):
     return ControllerUser.getUser(email)

@userAPI.get("/editar-usuario/{email}", tags=["usuarios"])
async def editarUsuario(email:str, Authorization: Annotated[Header, Depends(validar_token_admin)]):
     user = ControllerUser.getUser(email)
     return user # para carregar os dados do usuário encontrado na página (spa) de atualizar dados

@userAPI.patch("/atualizar-usuario", tags=["usuarios"]) 
async def atualizarUsuario(user:User, Authorization: Annotated[Header, Depends(validar_token_admin)]):
     return ControllerUser.updateUser(dict(user))

@userAPI.delete("/deletar-usuario/{email}", tags=["usuarios"])
async def excluirUsuarios(email:str, Authorization: Annotated[Header, Depends(validar_token_admin)]):
     return ControllerUser.deleteUser(email)

app.include_router(userAPI)