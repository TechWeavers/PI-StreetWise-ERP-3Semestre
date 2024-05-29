
from models.agendamentoModel import Agendamento
from configs.db import create_mongodb_connection
from services.Exceptions import Exceptions
from fastapi import HTTPException,status
from datetime import datetime, timezone
from dateutil import parser
from Controllers.Controller_Cliente import ControllerCliente
import datetime


# Configurações de conexão com o MongoDB
connection_string = "mongodb://localhost:27017/"
database_name = "streetwise_db"
collection_name = "agendamentos"

# Criando uma conexão com o MongoDB
db = create_mongodb_connection(connection_string, database_name)
collection = db[collection_name] 
class Controller_Copia_Agendamento():
  def __init__(self):
    pass

  def inserir_agendamento(self,agendamento:dict): 
    try:
         collection.insert_one(dict(agendamento)) 
    except HTTPException:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="cliente não encontrado nos registros do sistema")

  
  def getAllAgendamentos():
        try:
          agendamentos = [copias for copias in collection.find({})]  
          for copias in agendamentos:
            copias["_id"] = str(copias["_id"])

          return agendamentos
        except Exception as ex:
          return {"error": str({ex})}
        
  def getAgendamento(agendamentoId:str):
        try:
            agendamentos = collection.find({"id": agendamentoId})
            print(agendamentos)
            if not agendamentos:
               raise Exceptions("Erro ao buscar agendamento")
            
            found_agendamentos = []
            for evento in agendamentos:
                # Convert ObjectId to string if needed
                evento["_id"] = str(evento["_id"])
                found_agendamentos.append(evento)
            return found_agendamentos
        except Exception:
         raise Exceptions("Erro ao buscar agendamento")
        
  def deletarAgendamentos(self,eventId:str):
        try:
         query  = {"id":eventId}
         if not query:
            raise Exceptions("erro ao encontrar agendamento para deletar")
         result = collection.delete_one(query)
         if result:
               return {"message": " agendamento deletado com sucesso"}
        except Exception as ex:
          return {"error": str({ex})}

  def updateAgendamento(self,event:dict, eventId:str): 
        try:
            query = {"id": eventId}
            print(query)
            print(event)
            new_values = {"$set": event}
            print(new_values)
            result = collection.update_one(query, new_values)
            print(result)

            if result:
                return {"message": "agendamento atualizado com sucesso"}
            else:
                raise Exception("erro ao atualizar agendamento")
        except Exception:
            raise Exception("erro ao atualizar agendamento")
        
  @staticmethod
  def editarDados(agendamento_data:Agendamento):
      campos = ["id","nome", "descricao", "data", "hora_inicio","hora_fim","email_convidado"]
      print(agendamento_data)

      camposAtualizados = {}
      for campo in campos:
        if campo in agendamento_data and (agendamento_data[campo] is not None and agendamento_data[campo] != ""):
          camposAtualizados[campo] = agendamento_data[campo]
      return camposAtualizados
  
  @staticmethod
  def calcularProximosAgendamentos():
     data_atual = datetime.datetime.now()
     future_events = []
     agendamentos = collection.find({})
     
     for event in agendamentos:
          event["_id"] = str(event["_id"])
          start_time_str = event['start']['dateTime']
          start_time = parser.isoparse(start_time_str)

          if start_time > data_atual:
            future_events.append({"nome":event["summary"], "descrição":event["summary"]})

     return future_events
    
     