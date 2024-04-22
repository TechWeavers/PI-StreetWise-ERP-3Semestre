from typing import Annotated
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from models.userModel import User
from configs.db import create_mongodb_connection


SECRET_KEY = "FPaDbtjzU9r9kziJMkkkprJ8cVcEun6QyPf8XfSRdi2DJ56a6Wwhd32u9e8hdub" #assinatura do token
ALGORITHM = "HS256" # metodo utilizado pra codificar o token
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # tempo de expiração do token

# Configurações de conexão com o MongoDB
connection_string = "mongodb://localhost:27017/"
database_name = "streetwise_db"
collection_name = "users"

# Criando uma conexão com o MongoDB
db = create_mongodb_connection(connection_string, database_name)
collection = db[collection_name] # todas as operações de usuarios podem usar essa collection


def authenticate_user(username:str, password:str): # autenticar e retornar um usuário
    user = get_user(username)
    if not user:
        return False
    print(user["password"])
    if not verify_password(user["password"], user.hashed(password)):
        return False
    return user


def get_user (username: str):
    try:
        user = collection.find_one({"username":username})
        print(username)
        if user:
            print(user)
            return user
        else:
            return {"message":"usuario nao localizado"}
    except:
        print(f"Erro ao buscar usuário no MongoDB")
        return None

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto") # contexto passlib para fazer hash e verificação de senhas

def verify_password(plain_password, hashed_password): # verificar se a senha recebida corresponde ao hash armazenado
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password): # fazer hash de uma senha vinda do usuário
    return pwd_context.hash(password)


class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    username: str | None = None

def create_access_token(data:dict, expires_delta: timedelta | None = None): 
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
# verifica se o token já expirou, e se já, cria um novo token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# recebe um token jwt
# decodifica o token, verifica e retorna o usuário atual
# se o token for inválido, retorna um erro http
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(collection, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# autentica o usuário no banco de dados
#seta o tempo de expiração do token, e chama a função de criar token
#retorna o token
