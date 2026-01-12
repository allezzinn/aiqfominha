from fastapi import APIRouter, Depends, HTTPException # type: ignore
from models import Usuario
from dependencis import pegar_sessao
from main import bcrypt_context
from schemas import UsuarioSchema
from sqlalchemy.orm import Session # type: ignore

auth_router = APIRouter(prefix="/autenticação", tags=["autenticação"])

@auth_router.get("/")
async def home():
    #primeira linha da função como sendo a """Docstring for x"""
    """
    Essa é a rota padrão de autentificação, apenas retorna se o usuário está ou não eutentificado.
    """
    return {"mensagem": "Você está na rota padrão de autenticação.", "autenticado": False}

@auth_router.post("/criar_conta")
async def criar_conta(usuario_s: UsuarioSchema, session: Session= Depends(pegar_sessao)):  #Depends para "session" não passar como parâmetro para o usuário
    """Cria um novo usuário para o Banco de dados, tendo Ativo como default True e Admin como False"""
    # 1- abrir sessão no database (db) -> no arquivo dependencis.py
    # 2- Verificar se esse usuário já existe, pesquiso isso na tabela usuário
    usuario = session.query(Usuario).filter(Usuario.email==usuario_s.email).first() #Busca na tabela
    if usuario: 
        # email já cadastrado antes
        raise HTTPException(status_code=400, detail="Já existe um cadastro com esse e-mail.")   
        # irmão de erro do return    
    else:
        # criar novo usuario 
        senha_cripto= bcrypt_context.hash(usuario_s.senha)
        novo_usuario = Usuario(usuario_s.nome, usuario_s.email, senha_cripto, usuario_s.ativo, usuario_s.admin)
        session.add(novo_usuario)
        session.commit() # salva as informações 
        return {"mensagem": f"usuário {usuario_s.nome} cadastrado com sucesso"}