from fastapi import HTTPException, status, Depends
from jose import JWTError, jwt
from datetime import datetime, timedelta,timezone

SECRET_KEY = "FPaDbtjzU9r9kziJMkkkprJ8cVcEun6QyPf8XfSRdi2DJ56a6Wwhd32u9e8hdub" #assinatura do token
ALGORITHM = "HS256" # metodo utilizado pra codificar o token
ACCESS_TOKEN_EXPIRE_MINUTES = 600 # tempo de expiração do token

class Token:
    def __init__(self):
        pass

    def create_access_token(self,data:dict, expires_delta: timedelta | None = None): 
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(minutes=600)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def verificar_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError :
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado")
    # este método não está funcionando ainda





    
