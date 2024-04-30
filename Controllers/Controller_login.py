
import hashlib
from Controllers.token import Token
from services.Auth import Authenticator # importa o autenticador de usuário
from datetime import datetime, timedelta, timezone
from Controllers.token import ACCESS_TOKEN_EXPIRE_MINUTES,Token
from fastapi import HTTPException, status

class LoginController:
    def __init__(self):
        pass
    
    def login(self, user: str, password: str) -> str:
        jwt_token = Token()  
        auth = Authenticator()
      
        usuario = auth.authenticate_user(user,password)

        #if not usuario:
            #self.lancar_excecao_login()
        username = usuario["email"]
        print(username)
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
        credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Apenas administradores tem acesso a essa função",
        headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            jwt_token = Token() 
            jwt = jwt_token.verificar_token(token) 
            tipo =  jwt["sub"]
            if tipo=="Administrador":
                print(tipo)
                return jwt
            else:
                raise credentials_exception
        except Exception:
            raise credentials_exception
        
    def retornar_token(Authorization:str):
        jwt_token  = Token()
        token = jwt_token.verificar_token(Authorization)
        if not token:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
        return token
    
    

