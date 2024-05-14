import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class AgendaController:
    SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

    def __init__(self) -> None:
        self.creds = None
        self.service = None
        self.authenticate()

    def authenticate(self):
        if os.path.exists("token.json"):
            self.creds = Credentials.from_authorized_user_file("token.json", self.SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(self.creds.to_json())

            self.service = build("calendar", "v3", credentials=self.creds)

    def insertAgenda(self, agenda_data: dict):
        try:
            event = {
                'summary':"agenda teste controller", #f"{agenda_data['nome']}",
                'description':"teste cpntroller", #f"{agenda_data['desc']}",
                'start': {
                    'dateTime': (datetime.datetime.now() + datetime.timedelta(days=5)).replace(hour=14, minute=0).isoformat(),
                    'timeZone': 'America/Los_Angeles',
                },
                'end': {
                    'dateTime': (datetime.datetime.now() + datetime.timedelta(days=5)).replace(hour=16, minute=0).isoformat(),
                    'timeZone': 'America/Los_Angeles',
                },
                 'attendees': [
                {'email': 'contacomercial155@gmail.com'},
                ],
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},
                        {'method': 'popup', 'minutes': 10},
                    ],
                },
            }
            created_event = self.service.events().insert(calendarId='sixdevsfatec@gmail.com', body=event).execute()
            print('Event created: %s' % (created_event.get('htmlLink')))

        except HttpError as error:
            print(f"An error occurred: {error}")

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

    def deleteAgenda(self, agenda_ID):
        try:
            self.service.events().delete(calendarId='primary', eventId='eventId').execute()
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
