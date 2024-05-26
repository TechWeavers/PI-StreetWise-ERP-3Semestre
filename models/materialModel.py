from pydantic import BaseModel

class Material(BaseModel):
  nome: str
  quantidade: int
  valor_unitario: float | int | None = None
  data_atualizacao: str | None = None

