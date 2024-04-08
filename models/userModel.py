from pydantic import BaseModel
#from typing import Optional


class User(BaseModel): 
    # o id do usuario é gerado pelo próprio mongo
    username: str
    email:str
    senha:str
  


