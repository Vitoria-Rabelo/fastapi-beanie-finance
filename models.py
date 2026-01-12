from beanie import Document, Link
from beanie.odm.fields import PydanticObjectId
from pydantic import Field, BaseModel, EmailStr

# visao do banco de dados
class User(Document):
    nome: str
    email: EmailStr
    senha_hash: str

    class Settings:
        name = "users"

#visao dos usuarios finais
class User_Create(BaseModel):
    nome: str
    email: str
    senha: str

class Account(Document):
    nome: str
    tipo: str
    saldo_inicial: float
    usuario: Link["User"]

    class Settings:
        name = "accounts"

class AccountCreate(BaseModel):
    nome: str
    tipo: str
    saldo_inicial: float
    usuario_id: PydanticObjectId
    