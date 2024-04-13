
import datetime
def obterDataAtual():
  data_atual = datetime.datetime.now()
  dia = data_atual.strftime("%d")
  mes = data_atual.strftime("%m")
  ano = data_atual.strftime("%Y")
  data_format = dia+"/"+mes+"/"+ano
  return data_format
obterDataAtual()