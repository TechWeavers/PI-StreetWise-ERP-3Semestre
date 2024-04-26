from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from models.userLogin import UserLogin
from Controllers.Controller_login import LoginController


app = FastAPI()
userAPI = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

#contexto passlib para fazer hash e verificação de senhas
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")  

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@app.post("/login")
async def login_for_access_token(user_data: UserLogin) :
    controller = LoginController()
    return controller.login(user_data.username, user_data.password)
    

#@app.get("/users/me")
#async def read_users_me( current_user: Annotated[User, Depends(get_current_user  )]):
   # return current_user

# rota de teste como rota protegida   
#@app.get("/produto")
#async def obterProduto(token: str = Depends(get_current_user)):
    # Verifica se o token é válido e obtém os dados do usuário
    # user = await get_current_user(token)
    # print(user)"""
    
    # Se o token for válido, retorna os dados do produto
    #if token:
      #  return {"produto": {"nome": "mouse", "preço": 200}}
   # else:
    #    return{"message":"nao autorizado"}
