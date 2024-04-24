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

# valida o usuário no banco de dados e retorna ele
def authenticate_user(username:str, password:str): # autenticar e retornar um usuário
    user = get_user(username)
    if not user:
        return False
    print("Achou o usuário")

    if not verify_password(password, user["password"]):
        print("A senha está errada")
        return False
    print("A senha está certa")
    return user


def get_user (username: str):
    try:
        user = collection.find_one({"username":username})
        print(username)
        if user:
            return user
        else:
            print("usuario nao localizado")
            return None
    except:
        print("Erro ao buscar usuário no MongoDB")
        return None

# configurações do serviço de criptografia
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # contexto passlib para fazer hash e verificação de senhas

def verify_password(plain_password, hashed_password): # verificar se a senha recebida corresponde ao hash armazenado
    return pwd_context.verify(plain_password, get_password_hash(hashed_password))

def get_password_hash(password): # fazer hash de uma senha vinda do usuário
    return pwd_context.hash(password)

# configs do token
class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    username: str | None = None

# verifica se o token já expirou, e se já, cria um novo token
def create_access_token(data:dict, expires_delta: timedelta | None = None): 
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

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
            print(username)
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as erro:
        raise {"error": credentials_exception, "message":erro}
    user = get_user( username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# autentica o usuário no banco de dados
#seta o tempo de expiração do token, e chama a função de criar token
#retorna o token
