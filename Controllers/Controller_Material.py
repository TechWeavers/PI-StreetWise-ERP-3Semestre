from models.materialModel import Material
from configs.db import create_mongodb_connection
from services.Exceptions import Exceptions
from fastapi import HTTPException,status
import datetime
from typing import List

# Configurações de conexão com o MongoDB
connection_string = "mongodb://localhost:27017/"
database_name = "streetwise_db"
collection_name = "material"

db = create_mongodb_connection(connection_string, database_name)
collection = db[collection_name] 

class ControllerMaterial:
  def __init__(self) -> None:
    pass
    
  @staticmethod
  def insertMaterial(mat: Material):
      try:
        existingMaterial = collection.find_one({"nome":mat.nome})
        print(existingMaterial)
        if existingMaterial :
          raise ValueError("Já existe um material cadastrado com esse nome!")
        
        data_atual = datetime.datetime.now().strftime('%d/%m/%Y')
        mat.data_atualizacao = data_atual
        
        result = collection.insert_one(dict(mat))
        if not result:
          raise ValueError("Erro ao cadastrar material")
        return {"message": status.HTTP_200_OK}
      except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="já existe um material cadastrado com esse nome")
      except Exception:
        raise Exceptions.erro_manipular_material()
      
  @staticmethod
  def getAllMateriais():
         try:
            materiais = [mat for mat in collection.find({})]  
            for mat in materiais:
             mat["_id"] = str(mat["_id"])

            return {"materiais": materiais}
         except Exception:
          raise Exceptions.erro_manipular_material()
         

  @staticmethod
  def getMaterial(nome):
      try:
          materiais = collection.find({"nome":nome})
          print(materiais)
          if not materiais:
              raise Exceptions.erro_manipular_material()
          
          found_materiais = []
          for mat in materiais:
              # Convert ObjectId to string if needed
              mat["_id"] = str(mat["_id"])
              found_materiais.append(mat)
          return found_materiais
      except Exception:
        raise Exceptions.erro_manipular_material()
      

  @staticmethod
  def editMaterial(nome):
    try:
      material  = collection.find({"nome":nome})
      return material
    except Exception:
      raise Exceptions.erro_manipular_material()
        

  def updateMaterial(self, material: dict, nome:str): 
        try:
            query = {"nome":nome}
            dadosAtualizados = self.editarDados(material)

            new_values = {"$set": dadosAtualizados}
            print(new_values)
            result = collection.update_one(query, new_values)
            print(result)

            if result:
                return {"message": "material atualizado com sucesso"}
            else:
                raise Exceptions.erro_manipular_material()
        except Exception:
            raise Exceptions.erro_manipular_material()
        
  @staticmethod
  def editarDados(material_data:dict):
      campos = ["nome", "valor_unitario", "quantidade", "data_atualizacao"]
      data_atual = datetime.datetime.now().strftime('%d/%m/%Y')

      camposAtualizados = {}
      for campo in campos:
        if campo in material_data and (material_data[campo] is not None and material_data[campo] != ""):
          camposAtualizados[campo] = material_data[campo]
        if campo=="data_atualizacao":
                camposAtualizados[campo] = data_atual
      return camposAtualizados
  

  @staticmethod
  def deleteMaterial(nome):
    try:
      query  = {"nome":nome}
      if not query:
          raise Exceptions.erro_manipular_material()
      result = collection.delete_one(query)
      if result:
            return {"message": "material deletado com sucesso"}
      else:
            raise Exceptions.erro_manipular_material()
    except Exception:
      raise Exceptions.erro_manipular_material()

  @staticmethod
  def getMaterialConsumo(): # retorna a lista de materiais disponiveis com nome e quantidade
    try:
        materiais = collection.find({})

        materiais_dados_consumo = []
        for mat in materiais:
          materiais_dados_consumo.append({"nome":mat["nome"], "quantidade":mat["quantidade"]})

        return materiais_dados_consumo

    except:
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Erro ao buscar materiais para utilização")
    

  @staticmethod
  def consumirMateriais(materiais:List[Material]): # atualiza quantidade e data de atualização do material
    data_atual = datetime.datetime.now().strftime('%d/%m/%Y')
    try:
       for mat in materiais:
        nome = mat.nome
        quantidade_consumida = mat.quantidade
        material_cursor = collection.find_one({"nome":nome})

        quantidade_atual = material_cursor["quantidade"]
        quantidade_restante = quantidade_atual - quantidade_consumida
        
        query = {"nome":nome}
        new_value = {"$set": {"quantidade":quantidade_restante,"data_atualizacao":data_atual}}
        result = collection.update_one(query, new_value)
        print(result)

       return status.HTTP_200_OK

    except:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="erro ao utilizar materiais")
