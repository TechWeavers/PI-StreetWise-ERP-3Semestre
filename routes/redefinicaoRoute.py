from http.client import HTTPException
from fastapi import Depends, FastAPI, Header
from pydantic import BaseModel
from starlette.responses import JSONResponse
from routes.loginRoute import validar_token
from services.email import EmailSchema, emailEsqueceuSenha
from Controllers.Controller_user import ControllerUser
from fastapi.middleware.cors import CORSMiddleware
from Controllers.token import Token
from datetime import datetime, timedelta
from typing import Annotated
from models.emailModel import emailClass



app = FastAPI()
tokens = Token()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

import logging



class SenhaClass(BaseModel):
    senha: str
    senhaConfirmacao: str



@app.post("/EsqueceuSenha")
async def esqueceu_senha(email: emailClass) -> JSONResponse: #-> JSONResponse
    try:
        #for emailusuario in email.email:
        print(email)
        emailUsuario = email.email
        user = ControllerUser.getSingleUser(emailUsuario)
        
        print(user)
        if not user:
            raise HTTPException(404, f"Usuário não encontrado para o e-mail")
        
        #for user in users:
        ACCESS_TOKEN_EXPIRE_MINUTES=10
        access_token_expires = timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
        #jwt = jwt_token.create_access_token({"sub":usuario["tipo"]}, access_token_expires) 
        #return jwt
        token = tokens.create_access_token({"sub": emailUsuario},access_token_expires)
        print(token)
        await emailEsqueceuSenha(user,token) #, token
        return token
           
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(500, f"Erro ao enviar o e-mail: {str(e)}")

@app.post("/RedefinirSenha")
async def redefinir_senha(senhas:SenhaClass, Authorization: Annotated[Header, Depends(validar_token)]) -> JSONResponse:
    
    try:
        #token_data = tokens.verificar_token(Authorization)
        #print("tokeou")
        #if not token_data:
            #raise HTTPException(status_code=404, detail="Token inválido ou expirado")
        
        #if datetime.now(timezone.utc) > token_data["expiration_time"]:
            #del tokens[token]  
            #raise HTTPException(status_code=400, detail="Token expirado")
        
        if senhas.senha != senhas.senhaConfirmacao:
            raise HTTPException(status_code=400, detail="As senhas fornecidas são diferentes")
        
        user_data = {"email": token_data["email"], "password": senhas.senha}
        ControllerUser.updateUser(user_data)

        del tokens[token]

        return {"message": "Senha redefinida com sucesso"}

    except HTTPException as http_exception:
        raise http_exception

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao alterar a senha: {str(e)}")