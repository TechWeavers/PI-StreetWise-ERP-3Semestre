from datetime import datetime
import schedule
import time

# Importe suas rotas
from routes.comunicacaoRoute import enviar_email_24_horas_antes,enviar_email_24_horas_depois,enviar_email_retorno

# Função para agendar e executar suas rotas
def agendar_executar_rotas():
    # Adicione as rotas aqui
    enviar_email_24_horas_antes()
    enviar_email_24_horas_depois()
    enviar_email_retorno()
    
    # Substitua app.run() pelo método correto para executar suas rotas

# Agende a execução das rotas para ocorrer todos os dias às 02:56 da manhã
schedule.every().day.at("03:42").do(agendar_executar_rotas)

# Loop principal para manter o agendamento em execução
while True:
    schedule.run_pending()
    time.sleep(1)
