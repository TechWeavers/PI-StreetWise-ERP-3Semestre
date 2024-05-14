
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
  def __init__():
    pass

  def inserir_agendamento(self,agendamento:dict):
    try:
       collection.insert_one(dict(agendamento)) 
    except Exception as ex:
       return{"erro": str({ex})}
