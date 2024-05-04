from pydantic import BaseModel
from typing import Optional

class Cliente(BaseModel):
  nome: str
  cpf: str
  telefone:str
  email:str
  idade:str
  tratamento: Optional[bool] | None = None
  desc_tratamento: Optional[str] = None
  cirurgia: Optional[bool] = None
  desc_cirurgia: Optional[str]= None
  alergia: Optional[bool]= None
  desc_alergia: Optional[str]= None
  diabetes: Optional[bool]= None
  diabetes_desc: Optional[str]= None
  convulsao: Optional[bool]= None
  desc_convulsao: Optional[str]= None
  doencas_transmissiveis: Optional[bool]= None
  desc_doencas_transmissiveis: Optional[str]= None
  cardiaco: Optional[bool]= None
  cancer: Optional[bool]= None
  drogas: Optional[bool]= None
  pressao: Optional[bool]= None
  anemia: Optional[bool]= None
  hemofilia: Optional[bool] = None
  hepatite: Optional[bool]= None
  outro_desc: Optional[str] = None
  data_ficha : Optional[str] = None