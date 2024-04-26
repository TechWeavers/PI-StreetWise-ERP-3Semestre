
import hashlib
from Controllers.token import Token
from services.Auth import Authenticator # importa o autenticador de usuário
from datetime import datetime, timedelta, timezone
from Controllers.token import SECRET_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES,Token

class LoginController:
    def __init__(self):
        pass
    
    def login(self, user: str, password: str) -> bool:
        print(user)
        print(password)
        jwt_token = Token()  
        auth = Authenticator()
      
        usuario = auth.authenticate_user(user,password)
        username = usuario["username"]
        print(username)
        if usuario:
            senha_armazenada = usuario["password"]
            print(senha_armazenada)
            senha_criptografada = hashlib.sha256(password.encode()).hexdigest()
            print(senha_criptografada)
            
            if senha_armazenada == senha_criptografada:
                access_token_expires = timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
                jwt = jwt_token.create_access_token({"sub":user}, access_token_expires) 
                return [True,jwt,usuario]
        else:
            return False

    def user_id(self, token: str):
        jwt_token = Token() 
        payload = jwt_token.verificar_token(token) 
        return payload.get('sub')
    # este método não está em uso ainda