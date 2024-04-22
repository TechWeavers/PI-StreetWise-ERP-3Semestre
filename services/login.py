from Controllers.Controller_user import getUserbyUsername

def validarUsuario(username, password):
    user = getUserbyUsername(username)

    if user is None:
        return print("Usuário não encontrado")
    
    if password == user.password:
        return print("Senha Correta")
    else:
        return print("Senha incorreta")