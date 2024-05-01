from fastapi import HTTPException,status
class Exceptions(Exception):

  def __init__(self) -> None:
      pass

  @staticmethod
  def lancar_excecao_login():
    credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Usuário ou senha incorretos",
    headers={"WWW-Authenticate": "Incorrect Data"},)
    return credentials_exception
  
  @staticmethod
  def acesso_restrito_adm():
    credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Apenas administradores tem acesso a essa função",
    headers={"WWW-Authenticate": "Incorrect Data"},)
    return credentials_exception