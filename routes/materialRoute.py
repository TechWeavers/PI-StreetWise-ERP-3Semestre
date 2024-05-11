from fastapi import APIRouter, FastAPI, Depends,Header
from routes.loginRoute import validar_token, validar_token_admin
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from models.materialModel import Material
from Controllers.Controller_Material import ControllerMaterial

app = FastAPI()
materialAPI = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

@materialAPI.post("/novo-material", tags=["materiais"])
async def createMaterial(mat:Material,Authorization: Annotated[Header, Depends(validar_token_admin)]): #
    return ControllerMaterial.insertMaterial(mat)

@materialAPI.get("/listar-materiais", tags=["materiais"])
async def listarMateriais(Authorization: Annotated[Header, Depends(validar_token)]):
     return ControllerMaterial.getAllMateriais()

@materialAPI.get("/buscar-material/{nome}", tags=["materiais"]) 
async def buscarUsuario(nome:str, Authorization: Annotated[Header, Depends(validar_token)]):
    return ControllerMaterial.getMaterial(nome)

@materialAPI.patch("/atualizar-material/{nome}", tags=["materiais"]) 
async def atualizarCliente(mat:Material, nome:str ,Authorization: Annotated[Header, Depends(validar_token_admin)]):
     controller = ControllerMaterial()
     return controller.updateMaterial(dict(mat), nome)

@materialAPI.delete("/deletar-material/{nome}", tags=["materiais"])
async def excluirMaterial(nome:str, Authorization: Annotated[Header, Depends(validar_token_admin)]):
     return ControllerMaterial.deleteMaterial(nome)

app.include_router(materialAPI)


