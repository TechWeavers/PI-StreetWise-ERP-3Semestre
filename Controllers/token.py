from fastapi import HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta,timezone   
import logging


ACCESS_TOKEN_EXPIRE_MINUTES = 600 # tempo de expiração do token

class Token:
    def __init__(self):
        self.SECRET_KEY = "FPaDbtjzU9r9kziJMkkkprJ8cVcEun6QyPf8XfSRdi2DJ56a6Wwhd32u9e8hdub"
        self.ALGORITHM = "HS256" 

    def create_access_token(self,data:dict, expires_delta: timedelta | None = None): 
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(minutes=600)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def verificar_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            logging.error("Token expirado: %s", token)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado")
        except jwt.JWTError as e:
            logging.error("Erro ao decodificar token: %s", str(e))
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")   
    
    def retornar_token_admin(self,token:str):
        try:
            credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Apenas administradores tem acesso a essa função",
            headers={"WWW-Authenticate": "Bearer"},
            )
            token = self.verificar_token(token)
            tipo =  token["sub"]
            if tipo!="Administrador":
                raise credentials_exception
            else:
                print(tipo)
                return token     
        except Exception:
            raise credentials_exception
    
    # este método não está funcionando ainda





    
