from fastapi import APIRouter, Depends # type: ignore 
from sqlalchemy.orm import Session # type: ignore
from dependencis import pegar_sessao
from schemas import PedidoSchema
from models import Pedido

#deve passar: 1-Caminho 2-tags
order_router = APIRouter(prefix="/pedidos", tags=["pedidos"])
#para melhor organização e evitar conflitos de link
# @= decorator
#usar o roteador e definir nele o tipo e o caminho

@order_router.get("/") #= dominio/pedidos
async def pedidos():
    """
    Essa é a rota padrão de pedidos. Todas as rotas de pedidos precisam de autenticação
    """
    #o formato json funciona essencialmente com dicinários
    return {"mensagem": "Você está na rota pedidos"}

@order_router.post("/pedido")
async def criar_pedido(pedido_s: PedidoSchema, session: Session= Depends(pegar_sessao)):
    
    novo_pedido = Pedido(pedido_s.usuario)
    session.add(novo_pedido)
    session.commit()
    
    return {"mensagem": f"pedido criado com sucesso. Id do pedido {novo_pedido.id}."}