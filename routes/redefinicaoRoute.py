from http.client import HTTPException
from fastapi import FastAPI
from starlette.responses import JSONResponse
from services.email import EmailSchema, emailEsqueceuSenha
from Controllers.Controller_user import getUser
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.post("/EsqueceuSenha")
async def esqueceuSenha(email: EmailSchema) -> JSONResponse:
    try:
        for emailusuario in email.email:
            users = getUser(emailusuario)
            if not users:
                raise HTTPException(404, f"Usuário não encontrado para o e-mail: {emailusuario}")

            for user in users:
                await emailEsqueceuSenha(user)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(500, f"Erro ao enviar o e-mail: {str(e)}")

    return {"message": "E-mail enviado com sucesso"}