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
    MAIL_PASSWORD = "9243 2979",
    MAIL_FROM = "sixdevsfatec@gmail.com",
    MAIL_PORT = 465,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

app = FastAPI()

# mensagem enviada no email
html = """
<p>Thanks for using Fastapi-mail</p> 
"""

# rota que chama a função que envia o email
@app.post("/email")
async def simple_send(email: EmailSchema) -> JSONResponse:

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients= dict(email).get("email"),
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})  