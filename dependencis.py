from models import db
from sqlalchemy.orm import sessionmaker # type: ignore

# Sempre que necessário abrir uma sessão no banco de dados chamarei a mesma função, para evitar repetição de linhas de codigo, garantindo uma maior integridade do sistema
def pegar_sessao():
    try:
        Session = sessionmaker(bind=db) #cria a classe
        session = Session()    #cria a instância da classe

        yield session # retorna o valor mas sem encerrar a função (irmão irresponsável do return)
    
    finally: # executa independente se o try deu certo ou errado
        session.close() # fecha a sessão