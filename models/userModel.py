from pydantic import BaseModel
class User(BaseModel): 
    tipo:str
    name: str
    email:str 
    password:str
  


