import os.path
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from fastapi import HTTPException, status
from models.agendamentoModel import Agendamento
from Controllers.Controller_Agenda import Controller_Copia_Agendamento
from Controllers.Controller_Cliente import ControllerCliente

class GoogleCalendar:
    
    def __init__(self):
        self.creds = None
        self.SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
        self.token_path = "././token.json"
        self.credentials_path = "credentials.json"

    def auth_api(self):
        if os.path.exists(self.token_path):
            self.creds = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)
        
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                try:
                    self.creds.refresh(Request())
                except Exception as e:
                    print(f"Error refreshing token: {e}")
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            with open(self.token_path, "w") as token:
                token.write(self.creds.to_json())

        self.service = build("calendar", "v3", credentials=self.creds)

    def insert_event(self, evento: Agendamento):
        nome = evento.nome
        descricao = evento.descricao
        data = evento.data
        hora_inicio = evento.hora_inicio + ":00"
        hora_fim = evento.hora_fim + ":00"
        email_convidado = evento.email_convidado
        data  = self.formatar_data(data)
        print(data)

        try:
            self.auth_api()
            event = {
                'summary': nome,
                'description': descricao,
                'start': {
                    'dateTime': f"{data}T{hora_inicio}",
                    'timeZone': 'America/Sao_Paulo',
                },
                'end': {
                    'dateTime': f"{data}T{hora_fim}",
                    'timeZone': 'America/Sao_Paulo',
                },
                'attendees': [
                    {'email': email_convidado},
                ],
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},
                        {'method': 'popup', 'minutes': 10},
                    ],
                },
            }
            print("chegou aqui")
            
            if ControllerCliente.getClienteAgendamento(email_convidado):
                created_event = self.service.events().insert(calendarId='sixdevsfatec@gmail.com', body=event).execute()
                #print('Event created:', created_event.get('htmlLink'))
                copia_agendamento = event.copy()
                copia_agendamento["preco"] = evento.preco
                copia_agendamento["id"] = created_event['id']
                controller_agendamento = Controller_Copia_Agendamento()
                controller_agendamento.inserir_agendamento(copia_agendamento)
                return 200
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="cliente não encontrado nos registros do sistema")

        except HttpError as error:
            raise HTTPException(status_code=error.resp.status, detail=f"An error occurred: {error}")
        except Exception as erro:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"erro ao criar evento: {str(erro)}")

    def formatar_data(self, data: str):
        #try:
            data_atual = data.split("-")
            print(data_atual)
            dia = data_atual[2]
            mes = data_atual[1]
            ano = data_atual[0]
            data_format_final = f"{ano}-{mes}-{dia}"
            
            return data_format_final
    
        #except:
            #raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Erro ao encontrar data para agendamento")

    def deleteAgenda(self, event_ID):
        try:
            self.auth_api()
            self.service.events().delete(calendarId='sixdevsfatec@gmail.com', eventId=event_ID).execute()
            controller = Controller_Copia_Agendamento()
            controller.deletarAgendamentos(event_ID)
        except HttpError as error:
            print(f"An error occurred: {error}")

    def updateAgendamento(self, eventId: str, evento_atualizado: Agendamento):
        try:
            self.auth_api()
            event = self.service.events().get(calendarId='sixdevsfatec@gmail.com', eventId=eventId).execute()
            event['summary'] = evento_atualizado.nome
            event['description'] = evento_atualizado.descricao

            data_formatada = datetime.datetime.strptime(evento_atualizado.data, '%Y-%m-%d').strftime('%Y-%m-%d')
            event['start']['dateTime'] = f"{data_formatada}T{evento_atualizado.hora_inicio}:00"
            event['end']['dateTime'] = f"{data_formatada}T{evento_atualizado.hora_fim}:00"
            event['attendees'][0]['email'] = evento_atualizado.email_convidado

            self.service.events().update(calendarId='sixdevsfatec@gmail.com', eventId=eventId, body=event).execute()
            controller_copias = Controller_Copia_Agendamento()
            controller_copias.updateAgendamento(event, eventId)
            
        except HttpError as error:
            print(f"An error occurred: {error}")
