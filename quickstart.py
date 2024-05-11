
# ainda estou implementando a agenda do google no projeto
# vizera
import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]#.readonly


#def main():
"""Shows basic usage of the Google Calendar API.
Prints the start and name of the next 10 events on the user's calendar.
"""

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

try:
  service = build("calendar", "v3", credentials=creds)

  # Criação do evento
  event = {
        'summary': 'Evento Importante',
        'description': 'Este é um evento importante!',
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
  

  

    # Chama a API para criar o evento
  created_event = service.events().insert(calendarId='sixdevsfatec@gmail.com', body=event).execute()
  print('Event created: %s' % (created_event.get('htmlLink')))

  # teste chamando a cópia dos eventos
  #event_copia = created_event.copy()
  #print(event_copia)


  # Call the Calendar API
  now = datetime.datetime.now().isoformat() + "Z"  # 'Z' indicates UTC time
  print("Getting the upcoming 10 events")
  events_result = (
      service.events()
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
    #return None

  # Prints the start and name of the next 10 events
  for event in events:
    start = event["start"].get("dateTime", event["start"].get("date"))
    print(start, event["summary"])

  # Refer to the Python quickstart on how to setup the environment:
# https://developers.google.com/calendar/quickstart/python
# Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
# stored credentials.

  



    

except HttpError as error:
  print(f"An error occurred: {error}")


"""if __name__ == "__main__":
  main()"""