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