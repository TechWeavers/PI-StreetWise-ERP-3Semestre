from http.client import HTTPException
from typing import List
from fastapi import BackgroundTasks, FastAPI
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr
from starlette.responses import JSONResponse
from Controllers.Controller_user import User
from Controllers.Controller_Agenda import Controller_Copia_Agendamento
from models.clienteModel import Cliente
from datetime import datetime, timedelta
 
 
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

#Emails recuperação de senha

async def emailEsqueceuSenha(user: User,token:str): #, token: str
    try:
        emailusuario = user["email"]
        username = user["name"]
        redefinirURL = f"http://127.0.0.1:3000/redefinir-senha?token={token}"
 
        html = """
            <h1>Olá, {username}</h1>
            <p>Recebemos recentemente um pedido de recuperação de senha da sua conta cadastrada na InkDash</p>
            <br>
            <p>Se você não solicitou esse e-mail de redefinição de senha, não precisa se preocupar</p>
            <p>Basta ignorar esse e-mail</p>
            <br>
            <p>Clique no link abaixo para redefinir sua senha:</p>
            <p><a href="{redefinirURL}">Link para redefinição de senha</a></p>
            <br>
            <p>Este é um e-mail automático, não é preciso responder &#128521;</p>
            <p>Atenciosamente,</p>
            <p>Equipe da InkDash</p>
        """.format(username=username, redefinirURL= redefinirURL)
 
        message = MessageSchema(
            subject="Recuperação de Senha - InkDash",
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
            <p>Equipe da InkDash</p>
        """.format(username=user["name"])
 
        message = MessageSchema(
            subject="A redefinição de senha foi um sucesso! - InkDash",
            recipients=[emailusuario],
            body=html,
            subtype=MessageType.html
        )
 
        # Envio do e-mail
        await fm.send_message(message)
    except Exception as e:
        # Tratamento de exceções
        print("Erro ao enviar e-mail:", e)


#Emails procedimentos

async def email24Antes(email: str):
    try:
        emailusuario = email
       
        
        html = """
            <h1>Olá,</h1>
            <p>Este é um lembrete do seu agendamento de tatuagem na InkDash amanhã.</p>
            <br>
            <br>
            <p>Estamos ansiosos para vê-lo!</p>
            <p>Se você tiver alguma dúvida ou precisar reagendar, por favor entre em contato conosco.</p>
            <br>
            <p>Este é um e-mail automático, não é preciso responder &#128521;</p>
            <p>Atenciosamente,</p>
            <p>Equipe da InkDash</p>
        """
        
        message = MessageSchema(
            subject="Lembrete de Tatuagem Marcada - InkDash",
            recipients=[emailusuario],
            body=html,
            subtype=MessageType.html
        )
        
        # Envio do e-mail
        await fm.send_message(message)
    except Exception as e:
        # Tratamento de exceções
        print("Erro ao enviar e-mail:", e)

async def email24Depois(email: str):
    try:
        emailusuario = email
       
        
        html = """
            <h1>Olá!</h1>
            <p>Esperamos que você esteja satisfeito com sua nova tatuagem feita na InkDash!</p>
            <br>
            <p>Gostaríamos de saber se deu tudo certo com o procedimento. Caso tenha alguma dúvida ou preocupação, por favor, não hesite em nos contatar.</p>
            <br>
            <p>Aqui estão alguns cuidados importantes para garantir que sua tatuagem cicatrize bem:</p>
            <ul>
                <li>Mantenha a área tatuada limpa e hidratada.</li>
                <li>Evite exposição direta ao sol.</li>
                <li>Não submerja a tatuagem em água (banheiras, piscinas, etc.).</li>
                <li>Evite coçar ou arrancar casquinhas que possam se formar.</li>
            </ul>
            <br>
            <p>Estamos aqui para qualquer dúvida que você possa ter.</p>
            <p>Este é um e-mail automático, não é preciso responder &#128521;</p>
            <p>Atenciosamente,</p>
            <p>Equipe da InkDash</p>
        """
        
        message = MessageSchema(
            subject="Confirmação e Cuidados Pós-Tatuagem - InkDash",
            recipients=[emailusuario],
            body=html,
            subtype=MessageType.html
        )
        
        # Envio do e-mail
        await fm.send_message(message)
    except Exception as e:
        # Tratamento de exceções
        print("Erro ao enviar e-mail:", e)

async def emailRetorno(email: str):
    try:
        emailusuario =email
        
        
        html = """
            <h1>Olá,</h1>
            <p>Esperamos que você esteja gostando da sua nova tatuagem feita na InkDash!</p>
            <br>
            <p>Como parte do nosso plano de cuidados, gostaríamos de lembrá-lo sobre a possibilidade de realizar ajustes na sua tatuagem, caso seja necessário.</p>
            <p>É importante garantir que todos os detalhes estejam perfeitos e que a tatuagem esteja cicatrizando bem.</p>
            <br>
            <p>Por favor, entre em contato conosco para agendar um retorno. Estamos à disposição para qualquer ajuste que precise ser feito.</p>
            <br>
            <p>Este é um e-mail automático, não é preciso responder &#128521;</p>
            <p>Atenciosamente,</p>
            <p>Equipe da InkDash</p>
        """
        
        message = MessageSchema(
            subject="Retorno para Ajustes na Tatuagem - InkDash",
            recipients=[emailusuario],
            body=html,
            subtype=MessageType.html
        )
        
        # Envio do e-mail
        await fm.send_message(message)
    except Exception as e:
        # Tratamento de exceções
        print("Erro ao enviar e-mail:", e)

