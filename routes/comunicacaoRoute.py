from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from Controllers.Controller_Comunicacao_Email import Controller_Email

app = FastAPI()
comunicacaoAPI = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

@app.post("/email-24horas-depois")
async def mandar_email_24_horas_depois(): 
    controller_email = Controller_Email()
    return await controller_email.enviar_email_24_horas_antes()
   

@app.post("/email-24horas-antes")
async def mandar_email_24_horas_antes(): 
    controller = Controller_Email()
    return await controller.enviar_email_24_horas_depois()
    

