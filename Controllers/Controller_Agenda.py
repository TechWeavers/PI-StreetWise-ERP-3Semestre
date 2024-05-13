import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

service = build("calendar", "v3", credentials=creds)
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]#.readonly
# Configurações básicas pra rodar a API em qualquer método
creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists("token.json"):
  creds = Credentials.from_authorized_user_file("token.json", SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
  if creds and creds.expired and creds.refresh_token:
    creds.refresh(Request())
  else:
    flow = InstalledAppFlow.from_client_secrets_file(
        "credentials.json", SCOPES
    )
    creds = flow.run_local_server(port=0)
  # Save the credentials for the next run
  with open("token.json", "w") as token:
    token.write(creds.to_json())

class AgendaController:
    def __init__(self) -> None:
        pass

    def insertAgenda(agenda_data):

        try:
            event = {
                'summary': f"{agenda_data['nome']}",  # Utilizando f-string
                'description': f"{agenda_data['desc']}",
                'start': {
                    'dateTime': (datetime.datetime.now() + datetime.timedelta(days=5)).replace(hour=14, minute=0).isoformat(),
                    'timeZone': 'America/Los_Angeles',
                },
                'end': {
                    'dateTime': (datetime.datetime.now() + datetime.timedelta(days=5)).replace(hour=16, minute=0).isoformat(),
                    'timeZone': 'America/Los_Angeles',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},
                        {'method': 'popup', 'minutes': 10},
                    ],
                },
            }
            created_event = service.events().insert(calendarId='sixdevsfatec@gmail.com', body=event).execute()
            print('Event created: %s' % (created_event.get('htmlLink')))

        except HttpError as error:
            print(f"An error occurred: {error}")

    def getAllAgendamentos():
        try: 
            page_token = None
            while True:
                events = service.events().list(calendarId='primary', pageToken=page_token).execute()
                for event in events['items']:
                    print (event['summary'])
                page_token = events.get('nextPageToken')
                if not page_token:
                    break
        except HttpError as error:
            print(f"An error occurred: {error}")
    
    def deleteAgenda(agenda_ID):
        try:
            service.events().delete(calendarId='primary', eventId='eventId').execute()
        except HttpError as error:
            print(f"An error occurred: {error}")

    def updateAgendamento():
        try: 
            # First retrieve the event from the API.
            event = service.events().get(calendarId='primary', eventId='eventId').execute()

            event['summary'] = 'Appointment at Somewhere'

            service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
            print("update feito")
        except HttpError as error:
            print(f"An error occurred: {error}")
        
        #NADA AQUI FOI TESTADO OU IMPLEMENTADO AINDA