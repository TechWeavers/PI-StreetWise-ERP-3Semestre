from pydantic import BaseModel
 
class SenhaClass(BaseModel):
    senha: str
    senhaConfirmacao: str
 