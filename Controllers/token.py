from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
#import jwt 
from jose import JWTError, jwt
from datetime import datetime, timedelta
from services.Auth import Token, TokenData, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, create_access_token, get_current_user

SECRET_KEY = "FPaDbtjzU9r9kziJMkkkprJ8cVcEun6QyPf8XfSRdi2DJ56a6Wwhd32u9e8hdub" #assinatura do token
ALGORITHM = "HS256" # metodo utilizado pra codificar o token
class Token:
    def __init__(self):
        self.SECRET_KEY = "FPaDbtjzU9r9kziJMkkkprJ8cVcEun6QyPf8XfSRdi2DJ56a6Wwhd32u9e8hdub" #assinatura do token
        self.ALGORITHM = 'HS256'
        pass

    def verificar_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    def gerar_token(self, id: str) -> str:
        payload = {
            'sub': id,
            'exp': datetime.now() + timedelta(days=1) 
        }
        jwt_token = jwt.encode(payload, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return jwt_token
    
    # verifica se o token já expirou, e se já, cria um novo token
    def create_access_token(data:dict, expires_delta: timedelta | None = None): 
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    

    def criarToken(self, user):
        token = self.create_access_token(data={"sub": user}, expires_delta=timedelta(days=1))
        return token

    
