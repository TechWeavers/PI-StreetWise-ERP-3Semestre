from pymongo import MongoClient
 # cria uma conexão com o mongo db e chama o banco de dados
def create_mongodb_connection(connection_string, database_name):
    client = MongoClient(connection_string)
    db = client[database_name]
    return db


