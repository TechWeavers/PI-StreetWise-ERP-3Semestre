from fastapi import Depends, HTTPException, status
from models.userModel import User
import hashlib
from configs.db import create_mongodb_connection
from services.Exceptions import Exceptions

# Configurações de conexão com o MongoDB
connection_string = "mongodb://localhost:27017/"
database_name = "streetwise_db"
collection_name = "users"

# Criando uma conexão com o MongoDB
db = create_mongodb_connection(connection_string, database_name)
collection = db[collection_name] # todas as operações de usuarios podem usar essa collection

class Authenticator:
    def __init__(self):
       pass

    def authenticate_user(self,username:str, password:str): # autenticar e retornar um usuário
        
        #exception_login = Exceptions.lancar_excecao_login()
        try:
            user = self.get_user(username, password)
            if not user:
                raise Exceptions.lancar_excecao_login()
            print("Achou o usuário")

            senha_armazenada = user["password"]        
            if self.verificar_senha_encriptada(senha_armazenada,password):
                return user
            
        except Exception:
            raise Exceptions.lancar_excecao_login()
        

    # esta função pesquisa um usuário no banco por username e password (encriptado)
    def get_user (self,username: str, password:str):
        senha_criptografada = hashlib.sha256(password.encode()).hexdigest()
        user = collection.find_one({"username":username, "password":senha_criptografada})
        print(username)
        print(password)
        if user:
            user['_id'] = str(user['_id'])  # Convertendo o ObjectId para string
            return user
        else:
            print("usuario nao localizado")
            return False
        
    @staticmethod
    def verificar_senha_encriptada(senha_armazenada:str,password:str):
        print(senha_armazenada)
        senha_criptografada = hashlib.sha256(password.encode()).hexdigest()
        print(senha_criptografada)

        if senha_armazenada == senha_criptografada:
            return True
        return False
        
        
    
   
