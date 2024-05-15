
from models.agendamentoModel import Agendamento
from configs.db import create_mongodb_connection
from services.Exceptions import Exceptions
from fastapi import HTTPException,status


# Configurações de conexão com o MongoDB
connection_string = "mongodb://localhost:27017/"
database_name = "streetwise_db"
collection_name = "agendamentos"

# Criando uma conexão com o MongoDB
db = create_mongodb_connection(connection_string, database_name)
collection = db[collection_name] #todas as operações de usuarios podem usar essa collection

class Controller_Copia_Agendamento():
  def __init__(self):
    pass

  def inserir_agendamento(self,agendamento:dict): # este método é chamado de forma automática dentro do arquivo de controle da API, para criar uma cópia do agendamento
    try:
       collection.insert_one(dict(agendamento)) 
    except Exception as ex:
       return{"erro": str({ex})}

  @staticmethod
  def getAllAgendamentos():
        try:
          agendamentos = [copias for copias in collection.find({})]  
          for copias in agendamentos:
            copias["_id"] = str(copias["_id"])

          return agendamentos
        except Exception as ex:
          return {"error": str({ex})}
