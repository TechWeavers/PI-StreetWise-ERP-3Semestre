import schedule
import time
from datetime import datetime, timedelta
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

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


def enviar_email24HorasDepois(): # Agendar o envio do e-mail todos os dias às 01:30 da madrugada
  controller = Controller_Copia_Agendamento()
  agendamentos = controller.retornar_todos_agendamentos()

  # Obter a data atual
  data_atual = datetime.now()

  # Subtrair um dia da data atual para obter a data de ontem
  data_ontem = data_atual - timedelta(days=1)

  # Formatar a data de ontem no mesmo formato do objeto JSON
  data_ontem_formatada = data_ontem.strftime('%Y-%m-%dT%H:%M:%S')

  for event in agendamentos:
      if event["start"]["dateTime"] == data_ontem_formatada:
        email_cliente = event["attendees"][0]["email"]
        email24Depois(email_cliente)

  

# Loop para verificar a agenda e executar as funções agendadas
def verifica_agenda():
    while True:
        schedule.run_pending()
        time.sleep(1)

"""if __name__ == "__main__":
    # Iniciar o temporizador
    enviar_email24HorasDepois()"""

enviar_email24HorasDepois()
