from fastapi import APIRouter, Depends, HTTPException # type: ignore
from sqlalchemy.orm import Session # type: ignore
from dependencis import pegar_sessao, verificar_token
from schemas import PedidoSchema
from models import Pedido, Usuario

#deve passar: 1-Caminho 2-tags
order_router = APIRouter(prefix="/pedidos", tags=["pedidos"], dependencies=[Depends(verificar_token)])
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

@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session= Depends(pegar_sessao), usuario: Usuario= Depends(verificar_token)):
    # Verificar se o pedido existe e se pertence ao usuário autenticado
    # Usuário que podem cancelar pedidos: admin ou o próprio dono do pedido
    # usuario.admin = True ou usuario.id == pedido.usuario
    
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")
    
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem permissão para cancelar este pedido.")

    pedido.status = "CANCELADO"
    session.commit()
    return {
        "mensagem": f"Pedido {id_pedido} cancelado com sucesso.",
        "pedido": pedido
        }