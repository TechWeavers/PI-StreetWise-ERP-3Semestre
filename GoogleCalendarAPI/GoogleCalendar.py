import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from fastapi import HTTPException
from models.agendamentoModel import Agendamento
from Controllers.Controller_Agenda import Controller_Copia_Agendamento

# testando formatações de datas
data_atual = "15/05/2024"
data = data_atual.split("/")
dia  = data[0]
mes  = data[1]
ano  = data[2]
data_format = ano+"-"+mes+"-"+dia+"T"+"10:00:00"
data_format_final = ano+"-"+mes+"-"+dia+"T"+"15:00:00"


class GoogleCalendar():
    
    def __init__(self):
      self.creds = None
      self.SCOPES = ["https://www.googleapis.com/auth/calendar.events"]#.readonly
      self.token_path = "C:\\Users\\jpkun\\OneDrive\\Documentos\\3 SEMESTRE - FATEC\\PI-StreetWise-ERP-3Semestre\\GoogleCalendarAPI\\token.json"
      

    
    def auth_api(self):
      if os.path.exists(self.token_path):
        print("aaaaaaa")
        self.creds = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)
      print("chegu aqui 2")
      if not self.creds or not self.creds.valid:
          if self.creds and self.creds.expired and self.creds.refresh_token:
            self.creds.refresh(Request())
          else:
            print("chegou aqui 3")
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", self.SCOPES)
            print("chegou aqui 4")
            self.creds = flow.run_local_server(port=0)
            print("chegou aqui 4")
          with open("token.json", "w") as token:
            
            token.write(self.creds.to_json())

      self.service = build("calendar", "v3", credentials=self.creds)


    def insert_event(self, evento:Agendamento):
        nome = evento.nome
        descricao  = evento.descricao
        data= self.formatar_data(evento.data)
        hora_inicio = evento.hora_inicio+":00"
        hora_fim = evento.hora_fim+":00"
        email_convidado = evento.email_convidado
       
        try:
          self.auth_api()
          print("chegu aqui")
          print(data_format)
          event = {
              'summary': nome,
              'description': descricao,
              'start': {
                  'dateTime': data+"T"+hora_inicio,
                  'timeZone': 'America/Sao_Paulo',
              },
              'end': {
                  'dateTime': data+"T"+hora_fim,
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

          

          #copia_evento = event.copy()
        except Exception as erro:
           return {"erro aq chefia":str({erro})}
        
        created_event = self.service.events().insert(calendarId='sixdevsfatec@gmail.com', body=event).execute()
        print('Event created:', created_event.get('htmlLink'))
        print('ID do evento:', created_event['id'])
        copia_agendamento = event.copy()
        controller_agendamento = Controller_Copia_Agendamento()
        controller_agendamento.inserir_agendamento(copia_agendamento)
        
        

        """now = datetime.datetime.now().isoformat() + "Z"
        print("Getting the upcoming 10 events")
        events_result = (
            self.service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
        
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            print(start, event["summary"])"""
        
    def formatar_data(self,data:str):
       #data_atual = "15/05/2024"
       data_atual = data.split("/")
       dia  = data_atual[0]
       mes  = data_atual[1]
       ano  = data_atual[2]
       data_format = ano+"-"+mes+"-"+dia+"T"+"10:00:00"
       data_format_final = ano+"-"+mes+"-"+dia#+"T"+"15:00:00"
       return data_format_final

    def getAllAgendamentos(self):
        try: 
            page_token = None
            while True:
                events = self.service.events().list(calendarId='primary', pageToken=page_token).execute()
                for event in events['items']:
                    print(event['summary'])
                page_token = events.get('nextPageToken')
                if not page_token:
                    break
        except HttpError as error:
            print(f"An error occurred: {error}")

    def deleteAgenda(self, event_ID):
        try:
            self.auth_api()
            self.service.events().delete(calendarId='sixdevsfatec@gmail.com', eventId=event_ID).execute()
        except HttpError as error:
            print(f"An error occurred: {error}")

    def updateAgendamento(self):
        try: 
            event = self.service.events().get(calendarId='primary', eventId='eventId').execute()

            event['summary'] = 'Appointment at Somewhere'

            self.service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
            print("Update feito")
        except HttpError as error:
            print(f"An error occurred: {error}")


