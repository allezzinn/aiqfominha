# melhor Velocidade e integridade do sistema
from pydantic import BaseModel # type: ignore
from typing import Optional
# Semelhante a estrutura do models, mas apenas com as informações que o usuário PRECISA enviar
class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]
    # por padrão vai como dicionario

    class Config:
        from_attributes = True

class PedidoSchema(BaseModel):
    usuario: int

    class Config:
        from_attributes = True