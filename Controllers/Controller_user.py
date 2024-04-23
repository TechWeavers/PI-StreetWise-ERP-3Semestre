from configs.db import create_mongodb_connection
from models.userModel import User
from fastapi import HTTPException
from bson import json_util  # Importe o módulo bson


# Configurações de conexão com o MongoDB
connection_string = "mongodb://localhost:27017/"
database_name = "streetwise_db"
collection_name = "users"

# Criando uma conexão com o MongoDB
db = create_mongodb_connection(connection_string, database_name)
collection = db[collection_name] # todas as operações de usuarios podem usar essa collection

#insere um novo usuário no banco
def insertUser(user:User)->dict:
  try:
    collection.insert_one(dict(user))
    return {"message":"usuário cadastrado com sucesso","data":user}
  except TypeError as erro:
    return{"message":"erro ao cadastrar usuário","erro":str(erro)}
  except HTTPException(status_code=404,detail="Dados inválidos para cadastro") as error_http:
    return{"erro HTTP":error_http}
  

#obtém todos os usuários
def getAllUsers():
    try:
   # Obtendo todos os documentos da coleção como uma lista de dicionários
      users = [user for user in collection.find({})]  # pega cada elemento da collection e armazena na lista

    # Convertendo o campo '_id' para uma string em cada documento, é necessário para retornar 
      for user in users:
        user["_id"] = str(user["_id"])

      return {"users": users}
    except TypeError as erro:
      return{"Erro ao listar usuários: ":erro}

# por padrão pega o 1º elemento com o email especificado
def getUser(email):
  try:
    user_finded = [user for user in collection.find({"email":email})]
    for user in user_finded:
        user["_id"] = str(user["_id"])
  
    return user_finded
  except TypeError as erro:
    return{"erro ao buscar usuário: ":erro}

def editUser(email):
  try:
    user  = collection.find({"email":email})
    return user
  except TypeError as erro:
    return erro
  
def updateUser(user_data, email):
    try:
        query = {"email": email}
        new_values = {
            "$set": {
                "username": user_data["username"],
                "email": user_data["email"],
                "senha": user_data["senha"]
            }
        }
        result = collection.update_one(query, new_values)
        if result.modified_count > 0:
            return {"message": "Usuário atualizado com sucesso"}
        else:
            return {"message": "Nenhum usuário atualizado. Verifique o email fornecido."}
    except Exception as e:
        return {"erro": f"Erro ao atualizar usuário: {e}"}

def deleteUser(email):
  try:
    query  = {"email":email}
    collection.delete_one(query)
    return {"message":"usuário deletado com sucesso: "}
  except TypeError as erro:
    return{"erro ao deletar usuário: ":erro}


 