from fastapi import FastAPI # type: ignore 
from passlib.context import CryptContext # type: ignore
from dotenv import load_dotenv # type: ignore
import os
from fastapi.security import OAuth2PasswordBearer # type: ignore

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

app = FastAPI()
# código para rodar o código, execute no terminal: uvicorn main:app --reload
# esse é o único arquivo que devo me preocupar com a ordem da importação das coisas

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # garante o uso de modelos de criptografia seguros
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="autenticacao/login-form")  # o token deve ser passado com "header", não como "body"

from auth_routes import auth_router #autentificação
from order_routes import order_router #pedidos

#para imcluir no meu app as rotas que vem dos demais arquivos
app.include_router(auth_router) 
app.include_router(order_router)

@app.get("/")
async def inicio():
    return {"mensagem": "Nada para ver aqui, vá para /docs!"}