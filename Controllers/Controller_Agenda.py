
from models.agendamentoModel import Agendamento
from configs.db import create_mongodb_connection
from services.Exceptions import Exceptions
from fastapi import HTTPException,status
from datetime import datetime, timezone,timedelta
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

  quantidade_agendamentos = 0
  def __init__(self):
    pass

  def inserir_agendamento(self,agendamento:dict): 
    try:
         collection.insert_one(dict(agendamento)) 
         self.quantidade_agendamentos+=1
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
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Erro ao atualizar agendamento. Verifique os dados e tente novamente")
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
     
     contador = 0
     for event in agendamentos:
         
          event["_id"] = str(event["_id"])
          start_time_str = event['start']['dateTime']
          start_time = parser.isoparse(start_time_str)

          if start_time > data_atual and contador<=6:
            future_events.append({"nome":event["summary"], "descrição":event["description"]})
            contador+=1

     return future_events #retorna apenas os próximos 7 eventos
  
  
  def calcularQuantidadeAgendamentosnoMes(self):

    primeiro_dia_mes_atual  = self.obterPrimeiroDiadoMes()
    ultimo_dia_mes_atual  = self.obterUltimoDiadoMes()

    try:
      filtro = {"start.dateTime": {"$lte": ultimo_dia_mes_atual,"$gte":primeiro_dia_mes_atual}}
      total_documentos = collection.count_documents(filtro)
      
      return total_documentos
    except:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Não foi possível obter a quantidade de agendamentos no mês")
  
  @staticmethod
  def obterPrimeiroDiadoMes():
    data_atual = datetime.datetime.now()

    primeiro_dia_mes_atual = data_atual.replace(day=1, month=data_atual.month, hour=0, minute=0, second=0) 

    primeiro_dia_mes_atual = str(primeiro_dia_mes_atual)  
    primeiro_dia_mes_atual = primeiro_dia_mes_atual[:-7]
    print(primeiro_dia_mes_atual)
   
    return primeiro_dia_mes_atual
  
  @staticmethod
  def obterUltimoDiadoMes():
    data_atual = datetime.datetime.now()

    ultimo_dia_mes_atual = data_atual.replace(day=1, month=data_atual.month+1, hour=0, minute=0, second=0) - timedelta(days=1)

    ultimo_dia_mes_atual = str(ultimo_dia_mes_atual)
    ultimo_dia_mes_atual = ultimo_dia_mes_atual[:-7]
    print(ultimo_dia_mes_atual)
    
    return ultimo_dia_mes_atual
  
 
  def valorAgendamentosNoMes(self):
     
    primeiro_dia_mes_atual  = self.obterPrimeiroDiadoMes()
    ultimo_dia_mes_atual  = self.obterUltimoDiadoMes()
    filtro = {"start.dateTime": {"$lte": ultimo_dia_mes_atual,"$gte":primeiro_dia_mes_atual}}

    agendamentos_no_mes = []

    try:
      agendamentos = collection.find(filtro)

      for event in agendamentos:
        event["_id"] = str(event["_id"])
        agendamentos_no_mes.append(event)

      valor_bruto_agendamentos = 0
      for event in agendamentos_no_mes:
        valor_bruto_agendamentos = event["preco"]

      return valor_bruto_agendamentos
    
    except:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Erro ao carregar valor dos agendamentos no mês")
    

  def media_valor_agendamentos_no_mes(self):
     try:
      valor_bruto = self.valorAgendamentosNoMes()
      quantidade =self.calcularQuantidadeAgendamentosnoMes()
      media = valor_bruto/quantidade
      return media
     except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Erro ao carregar média do valor de agendamentos")
    
     
    
     