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
tokenClass = Token()
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
 
 
 
 
class SenhaClass(BaseModel):
    senha: str
    senhaConfirmacao: str
 
 
 
@app.post("/EsqueceuSenha")
async def esqueceu_senha(email: emailClass) -> str: 
    try:
        #for emailusuario in email.email:
        print(email)
        emailUsuario = email.email
        user = ControllerUser.getSingleUser(emailUsuario)
       
        print(user)
        if not user:
            raise HTTPException(404, f"Usuário não encontrado para o e-mail")
        ACCESS_TOKEN_EXPIRE_MINUTES=10
        access_token_expires = timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
        token = tokenClass.create_access_token({"sub": emailUsuario},access_token_expires)
        await emailEsqueceuSenha(user,token) #, token
        return token
           
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(500, f"Erro ao enviar o e-mail: {str(e)}")
 
@app.put("/RedefinirSenha")
async def redefinir_senha(senhas:SenhaClass, Authorization: Annotated[Header, Depends(validar_token)]) -> JSONResponse:
    print(Authorization)
    
    try:
        print("Authorization:", Authorization)
        #token_data = tokens.verificar_token(Authorization)
        #print("tokeou")
        #if not token_data:
            #raise HTTPException(status_code=404, detail="Token inválido ou expirado")
       
        #if datetime.now(timezone.utc) > token_data["expiration_time"]:
            #del tokens[token]  
            #raise HTTPException(status_code=400, detail="Token expirado")
        print(senhas.senha)
        if senhas.senha != senhas.senhaConfirmacao:
            raise HTTPException(status_code=400, detail="As senhas fornecidas são diferentes")

        user_data = {"email": Authorization["sub"], "password": senhas.senha}
        print("abu")
        print("user_data:", user_data)
        ControllerUser.updateUser(user_data)
        print("abu")
 
        return {"message": "Senha redefinida com sucesso"}
 
    except HTTPException as http_exception:
        raise http_exception
 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao alterar a senha: {str(e)}")