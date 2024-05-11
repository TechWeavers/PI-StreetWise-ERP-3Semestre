from fastapi import HTTPException,status
class Exceptions(Exception):

  def __init__(self) -> None:
      pass

  @staticmethod
  def user_senha_incorretos():
    credentials_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
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
  
  def token_invalido():
    credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Erro de autenticação de usuário, faça o login novamente!",
    headers={"WWW-Authenticate": "Incorrect Data"},)
    return credentials_exception
  
  def usuario_existente():
    credentials_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Já existe um usuário cadastrado com este email! Clique em redefinir senha ou se cadastre usando um novo email",)
    return credentials_exception
  
  def cliente_existente():
    credentials_exception = ValueError(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Já existe um cliente cadastrado com este CPF! ",)
    return credentials_exception
  
  def erro_manipular_usuario():
    credentials_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Erro ao manipular usuário no banco de dados",)
    return credentials_exception
  
  def erro_manipular_cliente():
    credentials_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Erro ao manipular cliente no banco de dados",)
    return credentials_exception
  
  def erro_manipular_material():
    credentials_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Erro ao manipular material no banco de dados",)
    return credentials_exception