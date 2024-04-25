from models.userModel import User
import hashlib
from Controllers.token import Token
from Controllers.Controller_user import getUser
from fastapi import Request
from configs.db import  create_mongodb_connection

# Configurações de conexão com o MongoDB
connection_string = "mongodb://localhost:27017/"
database_name = "streetwise_db"
collection_name = "users"

# Criando uma conexão com o MongoDB
db = create_mongodb_connection(connection_string, database_name)
collection = db[collection_name] # todas as operações de usuarios podem usar essa collection

class LoginController:
    def __init__(self):
        pass
        
    def get_user(self, username: str):
        try:
            user = collection.find_one({"username":username})
            print(username)
            if user:
                return user
            else:
                print("usuario nao localizado")
                return None
        except:
            print("Erro ao buscar usuário no MongoDB")
            return None

   
    
    def login(self, user: str, senha: str) -> bool:
        print(user)
        print(senha)
        jwt_token = Token()  
        #user_agent = request.headers.get("user-agent")
       # client_ip = request.client.host
        usuario = self.get_user(user)
        username = usuario["username"]
        print(username)
        if usuario:
            senha_armazenada = usuario["password"]
            print(senha_armazenada)
            senha_criptografada = hashlib.sha256(senha.encode()).hexdigest()
            print(senha_criptografada)
            
            if senha_armazenada == senha_criptografada:
                jwt = jwt_token.criarToken(username) 
                #print(jwt)
                return [True,jwt,usuario]
        else:
            return False

    def user_id(self, token: str):
        jwt_token = Token() 
        payload = jwt_token.verificar_token(token) 
        return payload.get('sub')