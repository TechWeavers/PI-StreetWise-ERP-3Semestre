
import hashlib
from Controllers.token import Token
from services.Auth import Authenticator # importa o autenticador de usuário
from datetime import datetime, timedelta, timezone
from Controllers.token import ACCESS_TOKEN_EXPIRE_MINUTES,Token
from fastapi import HTTPException, status
from services.Exceptions import Exceptions

class LoginController:
    def __init__(self):
        pass
    
    def login(self, email: str, password: str) -> str:
        jwt_token = Token()  
        auth = Authenticator()
      
        usuario = auth.authenticate_user(email,password)

        email = usuario["email"]
        print(email)
        if usuario:
            senha_armazenada = usuario["password"]
            print(senha_armazenada)
            senha_criptografada = hashlib.sha256(password.encode()).hexdigest()
            print(senha_criptografada)
            
            if senha_armazenada == senha_criptografada:
                access_token_expires = timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
                jwt = jwt_token.create_access_token({"sub":usuario["tipo"]}, access_token_expires) 
                return jwt
        else:
            return False

    def retornar_token_admin( token: str | None = None):
        try:
            jwt_token = Token() 
            jwt = jwt_token.verificar_token(token) 
            tipo =  jwt["sub"]
            if tipo=="Administrador":
                print(tipo)
                return jwt
            else:
                raise Exceptions.acesso_restrito_adm()
        except Exception:
            raise Exceptions.acesso_restrito_adm()
        
    def retornar_token(Authorization:str):
        jwt_token  = Token()
        token = jwt_token.verificar_token(Authorization)
        if not token:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
        return token
    
    

