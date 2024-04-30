from http.client import HTTPException
from typing import List
from fastapi import BackgroundTasks, FastAPI
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr
from starlette.responses import JSONResponse
from Controllers.Controller_user import User


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


fm = FastMail(conf)

html= ""

async def emailEsqueceuSenha(user: User,token:str): #, token: str
    try:
        emailusuario = user["email"]
        username = user["username"]
        redefinirURL = f"http://127.0.0.1:3000/redefinir-senha/{token}" 

        html = """
            <h1>Olá, {username}</h1>
            <p>Recebemos recentemente um pedido de recuperação de senha da sua conta cadastrada na InkHouse</p>
            <br>
            <p>Se você não solicitou esse e-mail de redefinição de senha, não precisa se preocupar</p>
            <p>Basta ignorar esse e-mail</p> 
            <br>
            <p>Clique no link abaixo para redefinir sua senha:</p>
            <p><a href="{redefinirURL}">Link para redefinição de senha</a></p>
            <br>
            <p>Este é um e-mail automático, não é preciso responder &#128521;</p>
            <p>Atenciosamente,</p>
            <p>Equipe da InkHouse</p>
        """.format(username=username, redefinirURL= redefinirURL)

        message = MessageSchema(
            subject="Recuperação de Senha - InkHouse",
            recipients=[emailusuario],
            body=html,
            subtype=MessageType.html
        )

        # Envio do e-mail
        await fm.send_message(message)
    except Exception as e:
        # Tratamento de exceções
        print("Erro ao enviar e-mail:", e)

async def senhaRedefinida(user: User): 
    try:
        emailusuario = user["email"]
        html = """
            <h1>Olá, {username}</h1>
            <p>Sua senha foi redefinida com sucesso</p>
            <p>Basta utilizar a nova senha cadastrada no link que te enviamos anteriormente</p> 
            <br>
            <p>Ps: Não esqueça de nunca compartilhar as suas senhas com ninguém.</p>
            <br>
            <p>Este é um e-mail automático, não é preciso responder &#128521;</p>
            <p>Atenciosamente,</p>
            <p>Equipe da InkHouse</p>
        """.format(username=user["username"])

        message = MessageSchema(
            subject="A redefinição de senha foi um sucesso! - InkHouse",
            recipients=[emailusuario],
            body=html,
            subtype=MessageType.html
        )

        # Envio do e-mail
        await fm.send_message(message)
    except Exception as e:
        # Tratamento de exceções
        print("Erro ao enviar e-mail:", e)
