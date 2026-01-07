from typing import Optional, TYPE_CHECKING
from beanie import Document, Link
from pydantic import BaseModel

# Isso avisa o VS Code que a classe User existe em outro lugar
if TYPE_CHECKING:
    from .user import User 

class Account(Document):
    nome: str
    tipo: str
    saldo_inicial: float
    # Use a string "User" dentro do Link para evitar erro de importação
    usuario: Link["User"] 

    class Settings:
        name = "accounts"