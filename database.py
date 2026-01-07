from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models.user import User
from models.category import Category
from models.transaction import Transaction
from models.account import Account

async def init_db():
    
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    
    # Inicializa o Beanie com os modelos
    await init_beanie(
        database=client.db_financeiro,
        document_models=[User, Category, Transaction, Account]
    )