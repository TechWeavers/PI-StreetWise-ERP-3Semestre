from pydantic import BaseModel

class Material(BaseModel):
  nome: str
  quantidade: int
  valor_unitario: float | int
  data_atualizacao: str | None = None