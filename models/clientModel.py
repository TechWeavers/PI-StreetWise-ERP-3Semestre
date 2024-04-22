from pydantic import BaseModel
from typing import Optional
import datetime

def obterDataAtual():
  data = datetime.datetime.now()
  dia = data.strftime("%d")
  mes = data.strftime("%m")
  ano = data.strftime("%Y")
  data_format = dia+"/"+mes+"/"+ano
  return data_format

data_atual = obterDataAtual

class Cliente(BaseModel):
  nome: str
  cpf: str
  telefone:int
  email:str
  nascimento:str
  tratamento: bool
  desc_tratamento: Optional[str]
  cirurgia: bool
  desc_cirurgia: Optional[str]
  alergia: bool
  desc_alergia: Optional[str]
  diabetes: bool
  diabetes_desc: Optional[str]
  convulsao: bool
  desc_convulsao: Optional[str]
  doencas_transmissiveis: bool
  desc_doencas_transmissiveis: Optional[str]
  cardiaco: bool
  cancer: bool
  drogas: bool
  pressao: bool
  anemia: bool
  hemofilia: bool 
  hepatite: bool
  outro_desc: Optional[str]
  data_ficha = Optional[str]