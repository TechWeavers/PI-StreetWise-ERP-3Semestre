from pydantic import BaseModel

"""event = {
              'summary': 'CHUPA MINHA BOLAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
              'description': 'TO CORINGANDODDDDDOOOOOOOOOO22222222222',
              'start': {
                  'dateTime': (datetime.datetime.now() + datetime.timedelta(days=1)).replace(hour=19, minute=0).isoformat(),
                  'timeZone': 'America/Sao_Paulo',
              },
              'end': {
                  'dateTime': (datetime.datetime.now() + datetime.timedelta(days=1)).replace(hour=21, minute=0).isoformat(),
                  'timeZone': 'America/Sao_Paulo',
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
          }"""
class Agendamento(BaseModel):
 id: str | None = None
 nome: str
 descricao: str
 data: str
 hora_inicio:str
 hora_fim:str
 email_convidado: str
 
