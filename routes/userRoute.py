from fastapi import APIRouter, FastAPI
from models.userModel import User
#importando controllers
from Controllers.Controller_user import insertUser,getAllUsers,getUser,deleteUser,updateUser

app = FastAPI()
userAPI = APIRouter()

@userAPI.post("/novo-usuario", tags=["usuarios"])
async def createUser(user:User):
     return insertUser(user)

@userAPI.get("/listar-usuarios", tags=["usuarios"])
async def listarUsuarios():
     return getAllUsers()

@userAPI.get("/buscar-usuario/{email}", tags=["usuarios"]) 
async def buscarUsuario(email:str):
     return getUser(email)
# buscando um usuario por email, pois é atributo unico

@userAPI.get("/editar-usuario/{email}", tags=["usuarios"])
async def editarUsuario(email:str):
     user = getUser(email) # busca o usuário para atualizar
     return user # para carregar os dados do usuário encontrado na página (spa) de atualizar dados

@userAPI.patch("/atualizar-usuario/{email}", tags=["usuarios"]) 
async def atualizarUsuario(user:User,email:str):
     return updateUser(dict(user),email)
# atualiza o usuario passando o parametro de busca pela URL, e chama a função de update

@userAPI.delete("/deletar-usuario/{email}", tags=["usuarios"])
async def excluirUsuarios(email:str):
     return deleteUser(email)

app.include_router(userAPI)