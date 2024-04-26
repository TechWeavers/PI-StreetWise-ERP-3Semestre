from pydantic import BaseModel
class UserLogin(BaseModel): # apenas para validação do login no sistema
    username: str
    password:str
  


