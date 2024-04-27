from pydantic import BaseModel
class User(BaseModel): 
    # o id do usuario é gerado pelo próprio mongo
    tipo:str
    username: str
    email:str 
    password:str
  


