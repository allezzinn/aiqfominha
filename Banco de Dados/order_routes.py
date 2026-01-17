from fastapi import APIRouter, Depends, HTTPException # type: ignore
from sqlalchemy.orm import Session # type: ignore
from dependencis import pegar_sessao, verificar_token
from schemas import PedidoSchema, ItemPedidoSchema
from models import Pedido, Usuario, ItemPedido

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

@order_router.put("/pedido/cancelar/{id_pedido}")
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
        "mensagem": f"Pedido {pedido.id} cancelado com sucesso.",
        "pedido": pedido
        }

@order_router.get("/listar")
async def listar_pedidos(session: Session= Depends(pegar_sessao), usuario: Usuario= Depends(verificar_token)):
    # Restringir essa rota apenas para administradores
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Acesso negado. Apenas administradores podem listar todos os pedidos.")
    else:
        pedidos = session.query(Pedido).all()
        return {
            "pedidos": pedidos
            }

@order_router.post("/pedido/adiciona-item/{id_pedido}")
async def adicionar_item_pedido(id_pedido: int, 
                                item_pedido_s: ItemPedidoSchema, 
                                session: Session= Depends(pegar_sessao), 
                                usuario: Usuario= Depends(verificar_token)):
    # Verificar se o pedido existe, achar o pedido
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido: 
        # se não exitir o pedido
        raise HTTPException(status_code=400, detail="Pedido não encontrado.")    
    elif not usuario.admin and usuario.id != pedido.usuario:
        # Verificar se o usuário tem permissão para adicionar itens (admin ou dono do pedido)
        raise HTTPException(status_code=401, detail="Você não tem permissão para adicionar itens a este pedido.")
    # Criar o novo item do pedido
    item_pedido = ItemPedido( item_pedido_s.quantidade,
        item_pedido_s.sabor,
        item_pedido_s.tamanho,
        item_pedido_s.preco_unitario,
        id_pedido)
    # Adicionar o item ao pedido e atualizar o preço total
    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {
        "mensagem": "Item adicionado ao pedido com sucesso.",
        "item_id": item_pedido.id,
        "pedido_id": id_pedido,
        "preco_atualizado": pedido.preco
        }