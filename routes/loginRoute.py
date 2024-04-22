from fastapi import APIRouter, FastAPI
from services.login import *

app = FastAPI()
userAPI = APIRouter()

@userAPI.get("/login", tags=["login"])
async def fazerLogin(user: str, password: str): #Dúvidas se será um dicionário ou só as variáveis
    return validarUsuario(user, password) 
