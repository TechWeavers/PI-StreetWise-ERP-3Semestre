from configs.db import create_mongodb_connection
from models.userModel import User
import hashlib
from services.Exceptions import Exceptions
from fastapi import HTTPException,status
import logging

# Configurações de conexão com o MongoDB
connection_string = "mongodb://localhost:27017/"
database_name = "streetwise_db"
collection_name = "users"

# Criando uma conexão com o MongoDB
db = create_mongodb_connection(connection_string, database_name)
collection = db[collection_name] #todas as operações de usuarios podem usar essa collection

class ControllerUser:
    def __init__(self) -> None:
      pass

    @staticmethod
    def insertUser(user:User)->dict:
      try:
        existingUser = collection.find_one({"email":user.email})
        if existingUser :
          raise Exceptions.usuario_existente()
  
        senha_criptografada = hashlib.sha256(user.password.encode()).hexdigest()
        user.password = senha_criptografada
        print(user)
        result = collection.insert_one(dict(user))
        if not result:
          raise ValueError("Erro ao manipular usuário")
        return {"message": status.HTTP_200_OK}
      except HTTPException:
        raise Exceptions.usuario_existente()
      except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Erro ao manipular usuário")
     
      
      
    
    @staticmethod
    def getAllUsers():
        try:
      # Obtendo todos os documentos da coleção como uma lista de dicionários
          users = [user for user in collection.find({})]  # pega cada elemento da collection e armazena na lista

        # Convertendo o campo '_id' para uma string em cada documento, é necessário para retornar 
          for user in users:
            user["_id"] = str(user["_id"])

          return {"users": users}
        except Exception:
         raise Exceptions.erro_manipular_usuario()

    @staticmethod
    def getUser(email):
        try:
            users = collection.find({"email": email})
            if not users:
               raise Exceptions.erro_manipular_usuario()
            
            found_users = []
            for user in users:
                # Convert ObjectId to string if needed
                user["_id"] = str(user["_id"])
                found_users.append(user)
            return found_users
        except Exception:
         raise Exceptions.erro_manipular_usuario()

    @staticmethod
    def getSingleUser(email):
        try:
            user = collection.find_one({"email": email})
            return user
        except Exception:
          raise Exceptions.erro_manipular_usuario()

    @staticmethod
    def editUser(email):
      try:
        user  = collection.find({"email":email})
        return user
      except Exception:
        raise Exceptions.erro_manipular_usuario()
      
    @staticmethod
    def updateUser(user_data):
        try:
            query = {"email": user_data["email"]}

            campos = ["name", "email", "tipo", "password"]

            camposAtualizados = {}
            for campo in campos:
              if campo in user_data and user_data[campo] is not None:
                  camposAtualizados[campo] = user_data[campo]

            new_values = {"$set": camposAtualizados}

            result = collection.update_one(query, new_values)

            if result.modified_count > 0:
                return {"message": "Usuário atualizado com sucesso"}
            else:
                raise Exceptions.erro_manipular_usuario()
        except Exception:
         raise Exceptions.erro_manipular_usuario()
        

    @staticmethod
    def update_user_senha(user_data):
        try:
            query = {"email": user_data["email"]}
            new_password = str(user_data["password"])
            senha_criptografada = hashlib.sha256(new_password.encode()).hexdigest()
            new_values = {"$set": {"password":senha_criptografada}}
            result = collection.update_one(query, new_values)

            if result.modified_count > 0:
                return {"message": "Usuário atualizado com sucesso"}
            else:
                raise Exceptions.erro_manipular_usuario()
        except Exception:
          raise Exceptions.erro_manipular_usuario()

    @staticmethod
    def deleteUser(email):
      try:
        query  = {"email":email}
        if not query:
           raise Exceptions.erro_manipular_usuario()
        result = collection.delete_one(query)
        if result:
            return {"message": "Usuário deletado com sucesso"}
        else:
            raise Exceptions.erro_manipular_usuario()
      except Exception:
        raise Exceptions.erro_manipular_usuario()


    