from fastapi import HTTPException, Depends # type: ignore
from models import db, Usuario
from sqlalchemy.orm import sessionmaker, Session # type: ignore
from jose import JWTError, jwt # type: ignore
from main import SECRET_KEY, ALGORITHM, oauth2_scheme

# Sempre que necessário abrir uma sessão no banco de dados chamarei a mesma função, para evitar repetição de linhas de codigo, garantindo uma maior integridade do sistema
def pegar_sessao():
    try:
        Session = sessionmaker(bind=db) #cria a classe
        session = Session()    #cria a instância da classe

        yield session # retorna o valor mas sem encerrar a função (irmão irresponsável do return)
    
    finally: # executa independente se o try deu certo ou errado
        session.close() # fecha a sessão

def verificar_token(token: str = Depends(oauth2_scheme), session: Session= Depends(pegar_sessao)):
    # veririfcar se o token é valido 
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM) # decodifica o token
        id_usuario = int(dic_info.get("sub")) # extrai o id do usuário do dicionário, chave "sub"
    except JWTError as erro:
        print(erro)
        raise HTTPException(status_code=401, detail="Acesso negado, token inválido, verifique a validade do token e tente novamente.")
    # extrair o id do usuário do token
    usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first() # valor default
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return usuario