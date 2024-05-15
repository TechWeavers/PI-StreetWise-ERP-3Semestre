
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

  
  def getAllAgendamentos():
        try:
          agendamentos = [copias for copias in collection.find({})]  
          for copias in agendamentos:
            copias["_id"] = str(copias["_id"])

          return agendamentos
        except Exception as ex:
          return {"error": str({ex})}
        
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

  def updateAgendamento(self,agendamento_data: Agendamento, eventId:str): 
        try:
            query = {"id": eventId}
            print(query)
            #dadosAtualizados = self.editarDados(agendamento_data)
            #print(dadosAtualizados)

            campos = ["id","nome", "descricao", "data", "hora_inicio","hora_fim","email_convidado"]
            camposAtualizados = {}
            for campo in campos:
              if campo in agendamento_data and (agendamento_data[campo] is not None and agendamento_data[campo] != ""):
                camposAtualizados[campo] = agendamento_data[campo]

            print(camposAtualizados)
            new_values = {"$set": camposAtualizados}
            print(new_values)
            result = collection.update_one(query, new_values)
            print(result)

            if result:
                return {"message": "agendamento atualizado com sucesso"}
            else:
                raise Exceptions("erro ao atualizar agendamento")
        except Exception:
            raise Exceptions("erro ao atualizar agendamento")
        
  @staticmethod
  def editarDados(agendamento_data:Agendamento):
      campos = ["id","nome", "descricao", "data", "hora_inicio","hora_fim","email_convidado"]
      print(agendamento_data)

      camposAtualizados = {}
      for campo in campos:
        if campo in agendamento_data and (agendamento_data[campo] is not None and agendamento_data[campo] != ""):
          camposAtualizados[campo] = agendamento_data[campo]
      return camposAtualizados