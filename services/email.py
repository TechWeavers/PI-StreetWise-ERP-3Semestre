from http.client import HTTPException
from typing import List
from fastapi import BackgroundTasks, FastAPI
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr
from starlette.responses import JSONResponse
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

# modelo de email a ser enviado
class EmailSchema(BaseModel):
    email: List[EmailStr]

# configurações de conexão com o email, está com bug na senha, que deve ser gerada pelo gmail
conf = ConnectionConfig(
    MAIL_USERNAME ="sixdevsfatec@gmail.com",
    MAIL_PASSWORD = "uzkh ccst nuza pkew",
    MAIL_FROM = "sixdevsfatec@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = False
)

# rota que chama a função que envia o email
@app.post("/email")
async def simple_send(email: EmailSchema) -> JSONResponse:
    try:
        for emailusuario in email.email:
            users = getUser(emailusuario)
            if not users:
                # Se nenhum usuário for encontrado para o e-mail, retorne uma mensagem de erro
                raise HTTPException(404, f"Usuário não encontrado para o e-mail: {emailusuario}")

            for user in users:
                # Construa o template de e-mail HTML com os dados do usuário
                html = f"""
                <h1>Olá, {user['username']}</h1>
                <p>Recebemos recentemente um pedido de recuperação de senha da sua conta cadastrada na InkHouse</p>
                <br>
                <p>Se você não solicitou esse e-mail de redefinição de senha, não precisa se preocupar</p>
                <p>Basta ignorar esse e-mail</p> 
                <br>
                <p>Clique no link abaixo para redefinir sua senha:</p>
                <p><a href="https://example.com/redefinir-senha">Link para redefinição de senha</a></p>
                <br>
                <p>Este é um e-mail automático, não é preciso responder &#128521;</p>
                <p>Atenciosamente,</p>
                <p>Equipe da InkHouse</p>
                """

                message = MessageSchema(
                    subject="Recuperação de Senha - InkHouse",
                    recipients=[emailusuario],
                    body=html,
                    subtype=MessageType.html
                )

                fm = FastMail(conf)
                await fm.send_message(message)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(500, f"Erro ao enviar o e-mail: {str(e)}")

    return {"message": "E-mail enviado com sucesso"}