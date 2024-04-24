from http.client import HTTPException
from typing import List
from fastapi import BackgroundTasks, FastAPI
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr
from starlette.responses import JSONResponse


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

app = FastAPI()

# mensagem enviada no email
html = """
    <h1>Olá, username</h1>
    <p>Recebemos recentemente um pedido de recuperação de senha da sua conta cadastrada na InkHouse</p>
    <br>
    <p>Se você não solicitou esse email de redefinição de senha, não precisa se preucupar</p>
    <p>Basta ignorar esse email</p> 
    <br>
    <p>Clique no link abaixo para redefinir sua senha:</p>
    <p><a href="https://example.com/redefinir-senha">Link para redefinição de senha</a></p>
    <br>
    <p>Este é um email automático, não é preciso responder &#128521;</p>
    <p>Atenciosamente,</p>
    <p>Equipe da InkHouse</p>
"""

# rota que chama a função que envia o email
@app.post("/email")
async def simple_send(email: EmailSchema) -> JSONResponse:

    message = MessageSchema(
        subject="Recuperação de Senha - InkHouse",
        recipients= dict(email).get("email"),
        body=html,
        subtype=MessageType.html
        )

    fm = FastMail(conf)
    print("passou")
    try:
        print("tentando")
        await fm.send_message(message)
    except Exception as e:
        raise HTTPException(500, "Erro ao enviar o email")
    return {"message": "Email enviado com sucesso"}