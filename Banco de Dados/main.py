from fastapi import FastAPI # type: ignore 
from passlib.context import CryptContext # type: ignore
from dotenv import load_dotenv # type: ignore
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI()
# código para rodar o código, execute no terminal: uvicorn main:app --reload
# esse é o único arquivo que devo me preocupar com a ordem da importação das coisas

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # garante o uso de modelos de criptografia seguros

from auth_routes import auth_router #autentificação
from order_routes import order_router #pedidos

#para imcluir no meu app as rotas que vem dos demais arquivos
app.include_router(auth_router)
app.include_router(order_router)

@app.get("/")
async def inicio():
    return {"mensagem": "Nada para ver aqui, vá para /docs !"}