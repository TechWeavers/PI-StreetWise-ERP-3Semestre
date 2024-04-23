from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import JWTError, jwt
from models.userModel import User
from configs.db import create_mongodb_connection
from services.Auth import Token, TokenData, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, create_access_token, get_current_user



app = FastAPI()
userAPI = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
# Configurações de conexão com o MongoDB
connection_string = "mongodb://localhost:27017/"
database_name = "streetwise_db"
collection_name = "users"

# Criando uma conexão com o MongoDB
db = create_mongodb_connection(connection_string, database_name)
collection = db[collection_name]  # todas as operações de usuários podem usar essa collection


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")  # contexto passlib para fazer hash e verificação de senhas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@app.post("/login")
async def login_for_access_token(user_data: User) -> Token:

    print(user_data.username)
    print(user_data.password)
    user = authenticate_user(user_data.username, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_data.username}, expires_delta=access_token_expires
    )
    return  Token(access_token=access_token, token_type="JWT")


@app.get("/users/me")
async def read_users_me(
    current_user: User = Depends(get_current_user),
):
    return current_user

@app.get("/produto")
async def obterProduto(token: str = Depends(get_current_user)):
    # Verifica se o token é válido e obtém os dados do usuário
    # user = await get_current_user(token)
    # print(user)"""
    
    # Se o token for válido, retorna os dados do produto
    if token:
        return {"produto": {"nome": "mouse", "preço": 200}}
    else:
        return{"message":"nao autorizado"}
