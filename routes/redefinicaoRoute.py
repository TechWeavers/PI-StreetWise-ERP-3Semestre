from http.client import HTTPException
from fastapi import Depends, FastAPI, Header
from pydantic import BaseModel
from starlette.responses import JSONResponse
from routes.loginRoute import validar_token
from services.email import EmailSchema, emailEsqueceuSenha
from Controllers.Controller_user import ControllerUser
from fastapi.middleware.cors import CORSMiddleware
from Controllers.token import *
from datetime import datetime, timedelta
from typing import Annotated



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
async def esqueceu_senha(email: EmailSchema) -> JSONResponse:
    try:
        for emailusuario in email.email:
            users = ControllerUser.getUser(emailusuario)
            if not users:
                raise HTTPException(404, f"Usuário não encontrado para o e-mail: {emailusuario}")

            for user in users:
                token = tokens.create_access_token(data={"email": emailusuario}, expires_delta=timedelta(minutes=30))
                await emailEsqueceuSenha(user, token)
        return {"message": "Token de redefinição de senha enviado com sucesso"}
           
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(500, f"Erro ao enviar o e-mail: {str(e)}")

@app.post("/RedefinirSenha")
async def redefinir_senha(senhas:SenhaClass, Authorization: Annotated[Header, Depends(validar_token)]) -> JSONResponse:
   

    try:
        token_data = tokens.verificar_token(Authorization)
        print("tokeou")
        if not token_data:
            raise HTTPException(status_code=404, detail="Token inválido ou expirado")
        
        if datetime.now(timezone.utc) > token_data["expiration_time"]:
            del tokens[token]  
            raise HTTPException(status_code=400, detail="Token expirado")
        
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