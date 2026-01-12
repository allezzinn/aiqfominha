from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey # type: ignore
from sqlalchemy.orm import declarative_base # type: ignore

#alembic, responsável pelo processo de migração (atualização do bd)
#sempre que quiser fazer uma migração, usar o comando "alembic revision --autogenerate -m "Seu texto aqui"  para criar a nova versão
#depois, para atualizar use o comando alembic upgrade head

#sqlalchemy - biblioteca instalada
# ORM - é possivel criar classes no python que são traduzidas para tabelas no banco de dados. Sendo possivel usar os dados do Banco simplesmente chamando essas classes construidas. Traduz comando em SQL para comando em python.

# cria a conexão (ending) do banco
db = create_engine("sqlite:///banco.db")

# cria a base do banco de dados
Base = declarative_base()

# criar as classes/tabelas do banco, elas serão na verdade subclasses da Base
#Usuarios
class Usuario(Base):
    __tablename__ = "usuarios"
    #cada campo vai ser uma columa no sqlalchemy
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String, nullable=False) #obrigatória preencher
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean, default=True) #parametro padrão
    admin = Column("admin", Boolean, default=False) #parametro padrão

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin #permite personalizar o valor de admin

# Pedidos
class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String)
    usuario = Column("usuario", ForeignKey("usuarios.id"))
    preco = Column("preco", Float)
    # itens = 

    def __init__ (self, usuario, status="PENDENTE", preco=0):
        self.usuario = usuario
        self.status = status
        self.preco = preco

# Itens Pedido
class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantidade = Column("quantidade", Integer)
    sabor = Column("sabor", String)
    tamanho = Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float)
    pedido = Column("pedido", ForeignKey("pedidos.id"))

    def __init__ (self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido

# executar a criação dos metadados do banco
