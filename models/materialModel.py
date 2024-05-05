from pydantic import BaseModel

class Material(BaseModel):
  nome: str
  quantidade: int
  valor_unitario: float
  data_atualizacao: str