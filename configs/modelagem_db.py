 

cliente = {
     "nome": "joão",
     "cpf": "45352257886",
     "telefone": "11988655418",
     "email": "jplima.dev@outlook.com",
     "ficha_anamnese": {
         "nascimento": "14/07/2004",
         "tratamento": "bronquite",
         "tratamento_desc": "aplicação de vacina semanal",
         "cirurgia": None,
         "cirurgia_desc": None,
         "alergia": None,
         "alerfia_desc": None,
         "diabetes": None,
         "diabetes_desc": None,
         "convulsao": None,
         "convulsao_desc": None,
         "doencas_transmissiveis": None,
         "doencas_transmissiveis_desc": None,
         "cardiaco": False,
         "cancer": False,
         "drogas": False,
         "cicatrizacao": True,
         "pressao": True,
         "anemia": True,
         "hemofilia": True,
         "hepatite": True,
         "outro": False,
         "outro_desc": False,
         "data_atual": "15/04/2024"

     }
 }

usuario = {
  "username":"vizera",
  "email":"jplima.dev@outlook.com",
  "senha":"admin123"
}

material = {
  "nome":"agulha",
  "valor_unit":23.50,
  "quantidade":5,
  "data_compra":"12/04/2024"
}

material_consumido = {
  "nome":"agulha",
  "quantidade":5,
  "valor total":50,
  "data_atual":"15/04/2024"
}

agendamento = {
  "summary": "Google I/O 2015",
  "location": "800 Howard St., San Francisco, CA 94103",
  "description": "A chance to hear more about Google\'s developer products.",
  "start": {
    "dateTime": "2015-05-28T09:00:00-07:00",
    "timeZone": "America/Los_Angeles",
  },
  "end": {
    "dateTime": "2015-05-28T17:00:00-07:00",
    "timeZone": "America/Los_Angeles",
  },
  "recurrence": [
    "RRULE:FREQ=DAILY;COUNT=2"
  ],
  "attendees": [
    {"email": "lpage@example.com"},
    {'email': "sbrin@example.com"},
  ],
  "reminders": {
    "useDefault": false,
    "overrides": [
      {"method": "email", "minutes": 24 * 60},
      {"method": "popup", "minutes": 10},
    ],
  },
}
