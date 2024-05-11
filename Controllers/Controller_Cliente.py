from models.clienteModel import Cliente
from configs.db import create_mongodb_connection
from services.Exceptions import Exceptions
from fastapi import HTTPException,status
import datetime

# Configurações de conexão com o MongoDB
connection_string = "mongodb://localhost:27017/"
database_name = "streetwise_db"
collection_name = "cliente"

# Criando uma conexão com o MongoDB
db = create_mongodb_connection(connection_string, database_name)
collection = db[collection_name] #todas as operações de usuarios podem usar essa collection

class ControllerCliente:
    def __init__(self):
      pass

    @staticmethod
    def insertCliente(cli: Cliente):
       try:
        existingCliente = collection.find_one({"cpf":cli.cpf})
        print(existingCliente)
        if existingCliente :
         raise ValueError("Já existe um cliente cadastrado com esse CPF!")
        
        result = collection.insert_one(dict(cli))
        if not result:
          raise ValueError("Erro ao manipular usuário")
        return {"message": status.HTTP_200_OK}
       except ValueError as e:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="já existe um usuário cadastrado com esse CPF")
       except Exception:
         raise Exceptions.erro_manipular_cliente()
       

    @staticmethod
    def getAllClientes():
         try:
            clientes = [cli for cli in collection.find({})]  
            for cli in clientes:
             cli["_id"] = str(cli["_id"])

            return {"clientes": clientes}
         except Exception:
          raise Exceptions.erro_manipular_cliente()
         
    @staticmethod
    def getCliente(cpf):
        try:
            clientes = collection.find({"cpf": cpf})
            print(clientes)
            if not clientes:
               raise Exceptions.erro_manipular_cliente()
            
            found_clientes = []
            for cli in clientes:
                # Convert ObjectId to string if needed
                cli["_id"] = str(cli["_id"])
                found_clientes.append(cli)
            return found_clientes
        except Exception:
         raise Exceptions.erro_manipular_cliente()
        
    @staticmethod
    def editCliente(cpf):
      try:
        cliente  = collection.find({"cpf":cpf})
        return cliente
      except Exception:
        raise Exceptions.erro_manipular_usuario()
      


    def updateCliente(self,cliente_data: dict, cpf:str): 
        try:
            query = {"cpf": cpf}
            """campos = ["nome", "cpf", "telefone", "email","idade"]

            camposAtualizados = {}
            for campo in campos:
                if campo in cliente_data and (cliente_data[campo] is not None and cliente_data[campo] != ""):
                    camposAtualizados[campo] = cliente_data[campo]"""
            dadosAtualizados = self.editarDados(cliente_data)

            new_values = {"$set": dadosAtualizados}
            print(new_values)
            result = collection.update_one(query, new_values)
            print(result)

            if result:
                return {"message": "Usuário atualizado com sucesso"}
            else:
                raise Exceptions.erro_manipular_cliente()
        except Exception:
            raise Exceptions.erro_manipular_cliente()
        
    @staticmethod
    def editarDados(cliente_data:dict):
       campos = ["nome", "cpf", "telefone", "email","idade"]

       camposAtualizados = {}
       for campo in campos:
          if campo in cliente_data and (cliente_data[campo] is not None and cliente_data[campo] != ""):
              camposAtualizados[campo] = cliente_data[campo]
       return camposAtualizados

       
        

    @staticmethod
    def deleteCliente(cpf):
      try:
         query  = {"cpf":cpf}
         if not query:
            raise Exceptions.erro_manipular_cliente()
         result = collection.delete_one(query)
         if result:
               return {"message": "Usuário deletado com sucesso"}
         else:
               raise Exceptions.erro_manipular_cliente()
      except Exception:
         raise Exceptions.erro_manipular_cliente()
      

    def salvarFicha(self,ficha_data: dict, cpf:str): 
        try:
         query = {"cpf": cpf}
         dadosAtualizados = self.editarFicha(ficha_data)
         new_values = {"$set": dadosAtualizados}
         result = collection.update_one(query, new_values)
         
         if result:
               return {"message": "ficha atualizada com sucesso"}
         else:
               raise Exceptions.erro_manipular_cliente()
        except Exception:
         raise Exceptions.erro_manipular_cliente()
        
    @staticmethod
    def editarFicha(ficha_data:dict):
         data_atual = datetime.datetime.now().strftime('%d/%m/%Y')
         print(data_atual)
         campos = ["tratamento","desc_tratamento", "cirurgia","desc_cirurgia," "alergia","desc_alergia","diabetes","desc_diabetes", "convulsao","desc_convulsao","doencas_transmissiveis","desc_doencas_transmissiveis","cardiaco","cancer","drogas","pressao","anemia","hemofilia","hepatite","outro_desc","data_atualizacao"]
         camposAtualizados = {}
         for campo in campos:
               if campo in ficha_data and (ficha_data[campo] is not None and ficha_data[campo] != ""):
                  camposAtualizados[campo] = ficha_data[campo]
               if campo=="data_atualizacao":
                  camposAtualizados[campo] = data_atual
         return camposAtualizados
      