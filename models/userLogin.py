from pydantic import BaseModel
class UserLogin(BaseModel): # apenas para validação do login no sistema
    email: str
    password:str
  


