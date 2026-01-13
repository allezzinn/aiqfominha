from fastapi import APIRouter, Depends, HTTPException # type: ignore
from models import Usuario
from dependencis import pegar_sessao, verificar_token
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session # type: ignore
from jose import JWTError, jwt # type: ignore
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm # type: ignore

auth_router = APIRouter(prefix="/autenticacao", tags=["autenticacao"])


def criar_token(id_usuario, duracao_token= timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    """Função para criar token de autentificação"""
    data_expira = datetime.now(timezone.utc) + duracao_token #data atual + tempo de expiração
    dic_info = {"exp": data_expira, 
                "sub": str(id_usuario)} # informações que vão dentro do token
    
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, algorithm=ALGORITHM) # cria o token codificado -> dicionaro/chave secreta/algoritmo
    return jwt_codificado

def autenticar_usuario(email, senha, session):
    """Função para autenticar usuário via token"""
    usuario = session.query(Usuario).filter(Usuario.email==email).first()

    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha): # se a senha não bater
        return False

    return usuario

@auth_router.get("/")
async def home():
    #primeira linha da função como sendo a """Docstring for x"""
    """
    Essa é a rota padrão de autentificação, apenas retorna se o usuário está ou não eutentificado.
    """
    return {"mensagem": "Você está na rota padrão de autenticacao.", "autenticado": False}

@auth_router.post("/criar_conta")
async def criar_conta(usuario_s: UsuarioSchema, session: Session= Depends(pegar_sessao)):  #Depends para "session" não passar como parâmetro para o usuário
    """Cria um novo usuário para o Banco de dados, tendo Ativo como default True e Admin como False"""
    # 1- abrir sessão no database (db) -> no arquivo dependencis.py
    # 2- Verificar se esse usuário já existe, pesquiso isso na tabela usuário
    usuario = session.query(Usuario).filter(Usuario.email==usuario_s.email).first() #Busca na tabela
    if usuario: 
        # email já cadastrado antes
        raise HTTPException(status_code=400, detail="Já existe um cadastro com esse e-mail.") # irmão de erro do return    
    else:
        # criar novo usuario 
        senha_cripto= bcrypt_context.hash(usuario_s.senha)
        novo_usuario = Usuario(usuario_s.nome, usuario_s.email, senha_cripto, usuario_s.ativo, usuario_s.admin)
        session.add(novo_usuario)
        session.commit() # salva as informações 
        return {"mensagem": f"usuário {usuario_s.nome} cadastrado com sucesso"}
    
@auth_router.post("/login")
async def login(login_s: LoginSchema, session: Session= Depends(pegar_sessao)):
    """Rota de login para autentificação do usuário"""
    
    usuario = autenticar_usuario(login_s.email, login_s.senha, session)

    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado.")
    else:
        acess_token = criar_token(usuario.id) 
        refresh_token = criar_token(usuario.id, duracao_token= timedelta(days=7)) # token de atualização com duração maior
        return {
            "access_token": acess_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"}
                
        #JWT - JSON Web Token - padrão de mercado para criação de tokens
        # JWT Bearer Token - padrão de mercado para autentificação via token
        # headers = {"Acess-Token": "bearer token_aqui"}

@auth_router.post("/login-form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session= Depends(pegar_sessao)):
    """Rota de login para autentificação do usuário"""
    
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)

    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado.")
    else:
        acess_token = criar_token(usuario.id) 
        return {
            "access_token": acess_token,
            "token_type": "bearer"}
                
        #JWT - JSON Web Token - padrão de mercado para criação de tokens
        # JWT Bearer Token - padrão de mercado para autentificação via token
        # headers = {"Acess-Token": "bearer token_aqui"}


@auth_router.get("/refresh_token")
async def use_refresh_token(usuario: Usuario= Depends(verificar_token)):
    # verificar o token 
    # gerar um novo token de acesso
    acess_token = criar_token(usuario.id)
    return {
        "access_token": acess_token,
        "token_type": "bearer"}
