from jose import  jwt
from datetime import datetime, timedelta,timezone   
from services.Exceptions import Exceptions


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
            
        except Exception:
            raise Exceptions.token_invalido()
    
    def retornar_token_admin(self,token:str):
        try:
            token = self.verificar_token(token)
            tipo =  token["sub"]
            if tipo!="Administrador":
                raise Exceptions.acesso_restrito_adm()
            else:
                print(tipo)
                return token     
        except Exception:
            raise Exceptions.acesso_restrito_adm()
        

    





    
